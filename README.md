# OntologyToAPI
> This project is an ontology-driven API generator designed for 
> backend development by transforming structured domain 
> knowledge into fully functional APIs. The tool accepts ontologies 
> specified in Turtle (.ttl), Resource Description Framework (.rdf)
> and Web Ontology Language (.owl).

## Ontological Framework:

- The following classes, relationships and data properties serve as a semantic blueprint for both metadata and business models.

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/main/Ontologies/2%20Smart-LEM%20Ontologies/Ontology%20Abstract%20Modules.jpg?raw=true" alt="AbstractOntologyClasses" title="Abstract Ontology Classes.">

## Installation and Running:

### Step 1: Prerequisites

- Make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

### Step 2: Creating a Virtual Environment (Jump to Step 3 if you already have one)

```bash
# Navigate to the directory where you want to use the package
cd repository/directory/path

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment (If you are on Windows)
.\venv\Scripts\activate

# Activate the virtual environment (If you are on Linux)
source venv/bin/activate
```

### Step 2: Installing the Package

```bash
# Now inside the environment install the python package
pip install OntologyToAPI
```

> From now on you must be ready to go and create your own ontological specification importing the Ontology Modules and extending it

### Step 4: Running

- To make your own ontological specification for this framework, please see the following documentations: TODO
- With you metadata and business models ontologies implemented you can generate your API by having the following python file as an entry point:

```python
import uvicorn
from core.APIGenerator import Generator

if __name__ == "__main__":
    APIGen = Generator(showLogs=True)
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

```python
import uvicorn
from core.APIGenerator import Generator

if __name__ == "__main__":
    APIGen = Generator(showLogs=True)
    # APIGen.load_ontologies(paths=[
    #     "Samples/PB_UseCase/RealizationOntologies/SmartLEM-PB_LEM.ttl",
    #     "Samples/PB_UseCase/RealizationOntologies/SmartLEM-EqualProsumerBiddingBusinessModel.ttl"
    # ])
    # APIGen.load_ontologies(paths=[
    #     "Samples/WeatherMonitoring_UseCase/RealizationOntologies/SmartLEM-Weather_LEM.ttl",
    #     "Samples/WeatherMonitoring_UseCase/RealizationOntologies/SmartLEM-WeatherBusinessModel.ttl"
    # ])
    APIGen.load_ontologies(paths=[
        "Samples/ASE_UseCase/RealizationOntologies/SmartLEM_LEMMembers.ttl",
        "Samples/ASE_UseCase/RealizationOntologies/SmartLEM_WeatherFromData.ttl",
        "Samples/ASE_UseCase/RealizationOntologies/SmartLEM-BusinessModels.ttl"
    ])
    APIGen.serialize_ontologies()
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)
```