from rdflib import Graph, Literal, URIRef
from typing import List
import logging
import pprint

logging.getLogger("rdflib").setLevel(logging.ERROR)

from Generator.Queries import *
from Generator.DTO.Metadata import *
from Generator.DTO.ExternalCode import *
from Generator.DTO.Source import *
from Generator.DTO.BusinessModel import *

from Generator.Connectors.IndentifyConnector import identifyConnector
from Generator.Utility import ensure_package_installed

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
            metadata_list = content.get("Metadata", [])
            for metadata in metadata_list:
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
            source = Source(desc=row[2], query=row[3])
            onto_pkg = self.g.qname(row[0]).split(":")[0]
            if onto_pkg not in data.keys(): data[onto_pkg] = {"Metadata": [], "CommTechnology": None}
            data[onto_pkg]["Metadata"].append(Metadata(name=self.g.qname(row[0]), type=row[1], hasSource=source))
            logging.info(f'{self.g.qname(row[0])} METADATA serialized successfully;')
        for comm in self.g.query(GET_COMMUNICATION_TECH_QUERY):
            comm_type = self.g.qname(comm[0]).split(":")[-1]
            comm_technology = comm[1]
            args = {self.g.qname(row[0]).split(":")[-1]: row[1] for row in self.g.query(GET_COMMUNICATION_TECH_ARGS_QUERY + URIRef(comm[-1]) + ">)}")}
            onto_pkg = self.g.qname(comm[2]).split(":")[0]
            if data[onto_pkg]["CommTechnology"] is None:
                data[onto_pkg]["CommTechnology"] = []
            data[onto_pkg]["CommTechnology"].append(identifyConnector(comm_type, comm_technology.value, args))
            logging.info(f'{onto_pkg}:{comm_type}:{comm_technology} CONNECTOR was configured successfully;')
        self.data = data

    def serialize_business_models(self):
        BMs = {}
        for ec in self.g.query(GET_EXTERNAL_CODE_FOR_BM_QUERY):
            bm_name = self.g.qname(ec[0])
            required_metadata = self._verify_metadata(GET_REQUIRED_MD_FOR_BM_QUERY + URIRef(ec[0]) + ">)}")
            results_metadata = self._verify_metadata(GET_RESULTS_MD_FOR_BM_QUERY + URIRef(ec[0]) + ">)}")
            for module in str(ec[3]).split(","): ensure_package_installed(module)
            BMs[bm_name] = BusinessModel(name=bm_name.split(":")[-1],
                               communications={pkg_name: pkg_data["CommTechnology"] for pkg_name, pkg_data in self.data.items()},
                               requiresMetadata=required_metadata,
                               resultsMetadata=results_metadata,
                               externalCode=ExternalCode(
                                    pythonFile=str(ec[2]),
                                    function=str(ec[4]),
                                    requiresLib=str(ec[3]).split(",")))
            logging.info(f'{bm_name} BUSINESS MODEL serialized successfully;')
        self.bms = BMs