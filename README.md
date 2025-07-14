# OntologyToAPI
> This project is an ontology-driven API generator designed for 
> backend development by transforming structured domain 
> knowledge into fully functional APIs. The tool accepts ontologies 
> specified in Turtle (.ttl), Resource Description Framework (.rdf)
> and Web Ontology Language (.owl).

## Ontological Framework:

- The following classes, relationships and data properties serve as a semantic blueprint for both metadata and business models.

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/main/Ontologies/2%20Smart-LEM%20Ontologies/Ontology%20Abstract%20Modules.jpg?raw=true" alt="AbstractOntologyClasses" title="Abstract Ontology Classes.">

## Use Case Application Sample:

- This application explores the generator functionalities in a Local Electricity Market using a locally hosted MySQL database and implements an Equal Prosumers Bidding Billing Algorithm.

### Ontology to represent the Metadata Realization of the Use Case and the Business Model

These ontologies can be found at: 
- [Use Case Ontology](https://github.com/JCGCosta/OntologyToAPI/blob/main/Samples/PB_UseCase/RealizationOntologies/SmartLEM-PB_LEM.ttl)
- [Business Model Ontology](https://github.com/JCGCosta/OntologyToAPI/blob/main/Samples/PB_UseCase/RealizationOntologies/SmartLEM-EqualProsumerBiddingBusinessModel.ttl)

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/main/Samples/PB_UseCase/RealizationOntologies/PB_UseCase%20Realization%20Ontology%20Diagram.jpg?raw=true" alt="RealizationOntologyClasses" title="Realization Ontology Classes.">

## Installation and Running:

### Step 1: Prerequisites

- Make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).
- Also make sure you have git installed in your machine. You can download git here: https://git-scm.com/downloads


### Step 2: Clone this repository

- Open your terminal or command prompt and navigate to the directory where you want to clone this repository. Then run the following command:

```bash
# Navigate to the directory where you want to create your project
git clone https://github.com/JCGCosta/OntologyToAPI.git
```

### Step 3: Creating a Virtual Environment

```bash
# Navigate to the directory where you cloned the repository
cd repository/directory/path

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment (If you are on Windows)
.\venv\Scripts\activate

# Activate the virtual environment (If you are on Linux)
source venv/bin/activate

# Now inside the environment install the libraries from the requirements.txt
pip install -r requirements
```

> From now on you must be ready to go and create your own ontological specification importing the modules

### Step 3: Running

- To make your own ontological specification for this framework, please see the following documentations: TODO
- With you metadata and business models ontologies implemented you can generate your API by having the following python file as an entry point:

```python
import uvicorn
from Generator.APIGenerator import Generator

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

### Step 3: Results

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/main/Samples/PB_UseCase/APIDocs.png?raw=true" alt="Output API" title="Output API.">

## Acknowledgements:

- This project is part of the Smart-LEM Consortium (https://smartlem.ase.ro).

> “This research was funded by FCT, under the scope of CETP/0003/2022 "Plataforma
baseada em modelos de negócio com aplicações para o desenvolvimento de
mercados de eletricidade locais e aceleração da transição energética".