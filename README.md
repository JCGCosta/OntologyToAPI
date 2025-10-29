# OntologyToAPI
> This project is an ontology-driven API generator designed for 
> backend development by transforming structured domain 
> knowledge into fully functional APIs. The tool accepts ontologies 
> specified in Turtle (.ttl), Resource Description Framework (.rdf)
> and Web Ontology Language (.owl).

> [![Publish to PyPI and TestPyPI](https://github.com/JCGCosta/OntologyToAPI/actions/workflows/python-publish.yml/badge.svg)](https://github.com/JCGCosta/OntologyToAPI/actions/workflows/python-publish.yml)


## Ontological Framework:

- The following classes, relationships and data properties serve as a semantic blueprint for both metadata and business models.

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/master/OntologicalFramework.jpg?raw=true" alt="AbstractOntologyClasses" title="Abstract Ontology Classes.">

The ontological framework is composed of four main modules:

  - **Metadata Ontology Module:** This module defines the essential classes and properties required to describe the metadata and its sources (e.g. Query to be executed on the CommunicationTechnology).
  - **BusinessModel Ontology Module:** This module captures the specific business logic and rules governing some operation, it requires an ExternalCode concretization, and it can require any metadata or parameter (To be sent in the API request).
  - **ExternalCode Ontology Module:** This module has all the technical details to connect to an external code, it also adds the possibility to dynamically require python packages.
  - **Communications Ontology Module:** This module describes the communication technologies that can be used to fetch the data of some metadata in multiple forms (e. g).

> From now on you must be ready to go and create your own ontological specification importing the [Ontology Modules](https://github.com/JCGCosta/OntologyToAPI/tree/master/OntologicalFramework) and extending it. You can do this by using the Protégé ontology editor (https://protege.stanford.edu/). Or if you prefer you can use any text editor to create your ontology files in the supported formats (.ttl, .rdf, .owl).

### Step 1: Installing the Package

```bash
pip install -U ontologytoapi
```

### Step 2: Running

- If you want to do a quick test we provided some .ttl samples at the following repository: https://github.com/JCGCosta/OntologyToAPISamples
- With your metadata and business models ontologies implemented you can generate your API by having the following python file as an entry point:

```python
import uvicorn
from OntologyToAPI.core.APIGenerator import APIGenerator

if __name__ == "__main__":
    APIGen = APIGenerator(showLogs=True)
    APIGen.load_ontologies(paths=[
        "Your/Metadata/Ontology/.ttl.owl.rdf"
    ])
    APIGen.load_ontologies(paths=[
        "Your/BusinessModel/Ontology/.ttl.owl.rdf"
    ])
    APIGen.serialize_ontologies()
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)
```
