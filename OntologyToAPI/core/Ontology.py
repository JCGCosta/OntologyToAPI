from rdflib import Graph, URIRef
from pathlib import Path
import logging
import pprint

logging.getLogger("rdflib").setLevel(logging.ERROR)

from OntologyToAPI.core.Queries import *
from OntologyToAPI.core.DTO.Source import *
from OntologyToAPI.core.DTO.BusinessModel import *

from OntologyToAPI.core.Connectors.IndentifyConnector import identifyConnector
from OntologyToAPI.core.Utility import ensure_package_installed

class Ontology:
    def __init__(self):
        self.g = Graph()
        self.data = {}
        self.bms = {}

    def parse_ontology(self, path: str):
        if path.endswith('.ttl'):
            self.g.parse(path, format='turtle')
        elif path.endswith('.owl') or path.endswith('.rdf'):
            self.g.parse(path, format='xml')
        else:
            raise ValueError(f'File extension must be .ttl or .owl or .rdf ({path} could not be parsed)')
        logging.info(f'Ontology \"{path}\" parsed successfully.')

    def __repr__(self):
        return (f"data(\n{pprint.pformat(self.data, indent=2)}\n)\n"
                f"business_models(\n{pprint.pformat(self.bms, indent=2)}\n)")

    def _get_metadata_by_name(self, name: str):
        for namespace, content in self.data.items():
            for metadata in content:
                if metadata.name == name:
                    return metadata
        return None

    def _verify_metadata(self, q: str):
        md = []
        for row in self.g.query(q):
            metadata_obj = self._get_metadata_by_name(self.g.qname(row[1]))
            if not metadata_obj:
                raise ValueError(
                    f'The {self.g.qname(row[1])} metadata which is required by the {self.g.qname(row[0])} could not be found in the ontology.')
            md.append(metadata_obj)
        return md

    def serialize_metadata(self):
        data = {}
        for row in self.g.query(GET_METADATA_QUERY):
            args = {self.g.qname(row[0]).split(":")[-1]: row[1] for row in
                    self.g.query(GET_COMMUNICATION_TECH_ARGS_QUERY + URIRef(row[4]) + ">)}")}
            comm_tech = identifyConnector(row[5], args)
            source = Source(desc=row[2], query=row[3], comm_technology=comm_tech)
            onto_pkg = self.g.qname(row[0]).split(":")[0]
            if onto_pkg not in data.keys(): data[onto_pkg] = []
            data[onto_pkg].append(Metadata(name=self.g.qname(row[0]), type=row[1], hasSource=source))
            logging.info(f'{self.g.qname(row[0])} METADATA serialized successfully;')
        self.data = data

    def serialize_business_models(self):
        BMs = {}
        for ec in self.g.query(GET_EXTERNAL_CODE_FOR_BM_QUERY):
            bm_name = self.g.qname(ec[0])
            required_metadata = self._verify_metadata(GET_REQUIRED_MD_FOR_BM_QUERY + URIRef(ec[0]) + ">)}")
            required_parameters = self.g.query(GET_REQUIRED_PARAMETERS_FOR_BM_QUERY + URIRef(ec[0]) + ">)}")
            for module in str(ec[3]).split(","): ensure_package_installed(module)
            func_path = Path(str(ec[2])).expanduser()
            if not func_path.is_absolute(): func_path = (Path.cwd() / func_path).resolve(strict=False)
            else: func_path = func_path.resolve(strict=False)
            if not func_path.exists() or not func_path.is_file():
                raise FileNotFoundError(f'The external code file for the {bm_name} business model could not be found at "{func_path}"')
            BMs[bm_name] = BusinessModel(name=bm_name.split(":")[-1],
                               requiresMetadata=required_metadata,
                               requiresParameters={str(l): t for _, l, t in required_parameters},
                               externalCode=ExternalCode(
                                    pythonFile=str(func_path),
                                    function=str(ec[4]),
                                    requiresLib=str(ec[3]).split(",")))
            logging.info(f'{bm_name} BUSINESS MODEL serialized successfully;')
        self.bms = BMs