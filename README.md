# OntologyToAPI
> This python package is an ontology-driven API generator designed for 
> backend development by transforming structured domain 
> knowledge, different data sources and implemented business models into fully functional APIs. The tool accepts ontologies 
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

> A full documentation on how to extend your own ontologies using the OntologyToAPI framework is still in development, but you can check the example provided below. Or at https://github.com/JCGCosta/OntologyToAPI/tree/master/example

## Installing the Package

```bash
pip install -U ontologytoapi
```

## Running a Simple Example

- Ontology file with triples to a weather use case extending the OntologyToAPI framework:

```turtle
# ./metadata_example.ttl

@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

@prefix md:  <http://www.cedri.com/OntologyToAPI-Metadata#> .
@prefix comm:  <http://www.cedri.com/OntologyToAPI-Communications#> .

@prefix ex:   <http://example.org/> .

# Class Definitions

ex:Temperature_C rdf:type owl:Class ;
          rdfs:subClassOf md:Metadata ;
          rdfs:comment "A measure of the average kinetic energy of the particles within a substance, which corresponds to its hotness or coldness." .

ex:Relative_Humidity rdf:type owl:Class ;
          rdfs:subClassOf md:Metadata ;
          rdfs:comment "The ratio of the amount of water vapor currently in the air to the maximum amount the air could hold at that specific temperature, expressed as a percentage." .

# Individuals for Metadata and Communication

ex:SQLITE_DB rdf:type owl:NamedIndividual ,
                      comm:DatabaseCommunication ;
             comm:hasConnectionString "sqlite+aiosqlite:///example.db" ;
             comm:usesTechnology "SQLITE" .

ex:Temperature_C_Source rdf:type owl:NamedIndividual ,
                      md:Source ;
             md:hasCommunicationTechnology ex:SQLITE_DB ;
             md:hasDescription "Retrieves the temperature data from a local SQLite database." ;
             md:hasQuery "SELECT temperature_c FROM weather;" .

ex:Temperature_C_MD rdf:type owl:NamedIndividual ,
                           ex:Temperature_C ;
                  md:hasSource ex:Temperature_C_Source ;
                  md:hasType "float" .

ex:Relative_Humidity_Source rdf:type owl:NamedIndividual ,
                      md:Source ;
             md:hasCommunicationTechnology ex:SQLITE_DB ;
             md:hasDescription "Retrieves the relative humidity data from a local SQLite database." ;
             md:hasQuery "SELECT r_humidity FROM weather;" .

ex:Relative_Humidity_MD rdf:type owl:NamedIndividual ,
                           ex:Relative_Humidity ;
                  md:hasSource ex:Relative_Humidity_Source ;
                  md:hasType "float" .
```

- Ontology file with triples to represent temperature convertion sample in the OntologyToAPI framework:

```turtle
# ./bm_example.ttl

@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

@prefix md:  <http://www.cedri.com/OntologyToAPI-Metadata#> .
@prefix comm:  <http://www.cedri.com/OntologyToAPI-Communications#> .
@prefix bm:  <http://www.cedri.com/OntologyToAPI-BusinessModel#> .
@prefix excode:  <http://www.cedri.com/OntologyToAPI-ExternalCode#> .

@prefix ex:   <http://example.org/> .

# Class Definitions

ex:CelsiusToFahrenheit rdf:type owl:Class ;
                       rdfs:subClassOf bm:BusinessModel ;
                       rdfs:comment "This business model allows the convertion from Celsius to Fahrenheit." .

# Individuals for Business Models

ex:CelsiusToFahrenheit.py rdf:type owl:NamedIndividual ,
                                   excode:ExternalCode ;
                          excode:hasFunction "convert_temperature_c_to_f" ;
                          excode:hasPythonFile "bm.py" ;
                          excode:requiresLib "requests" .

ex:Temperature_P rdf:type owl:NamedIndividual ,
                          bm:Parameter ;
                 bm:hasParameterLabel "temperature_c" ;
                 bm:hasParameterType "float" .

ex:CelsiusToFahrenheit_I rdf:type owl:NamedIndividual ,
                                  ex:CelsiusToFahrenheit ;
                         bm:requiresMetadata ex:Temperature_C_MD;
                         bm:hasExternalCode ex:CelsiusToFahrenheit.py ;
                         bm:hasParameter ex:Temperature_P .
```

- Code to have the business model implementation:

```python
# ./bm.py

async def convert_temperature_c_to_f(data):
    if not data.metadata and data.params["temperature_c"] is None:
        return {"error": "No temperature was provided from Metadata or from the endpoint Parameters."}
    if data.params["temperature_c"] is not None:
        return {
            "original": data.params["temperature_c"],
            "converted": data.params["temperature_c"] * 9 / 5 + 32
        }
    else:
        return {
            "original": [t["temperature_c"] for t in data.metadata["Temperature_C_MD"]],
            "converted": [t["temperature_c"] * 9 / 5 + 32 for t in data.metadata["Temperature_C_MD"]]
        }
```

- Code to generate the API:

```python
# ./main.py

import uvicorn
import sqlite3
from pathlib import Path
from OntologyToAPI.core.APIGenerator import APIGenerator

def configuring_a_sample_sqlite_database():
    if not Path('example.db').exists():
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature_c FLOAT NOT NULL,
                    r_humidity FLOAT NOT NULL
                );
            ''')
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('21.5', '60');")
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('22.0', '58');")
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('20.8', '65');")
            conn.commit()

if __name__ == "__main__":
    configuring_a_sample_sqlite_database()
    APIGen = APIGenerator(showLogs=True)
    APIGen.load_ontologies(paths=[
        "metadata_example.ttl",
        "bm_example.ttl"
    ])
    APIGen.serialize_ontologies()
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)
```

- Your project structure should look something like this:

```
├── metadata_example.ttl
├── bm_example.ttl
├── bm.py
├── main.py
```

- Then you should be able to run the example as follows:

```bash
# To run the example, then execute:
python main.py

# You can access the API documentation at: http://localhost:5000
```

> From now on you must be ready to go and create your own ontological specification importing the [Ontology Modules](https://github.com/JCGCosta/OntologyToAPI/tree/master/OntologicalFramework) and extending it. You can do this by using the Protégé ontology editor (https://protege.stanford.edu/). Or if you prefer you can use any text editor to create your ontology files in the supported formats (.ttl, .rdf, .owl).


## Supported communication technologies are (Currently):

#### Stateful Connections
- "SOCKET" - For Socket connections using asyncio streams

#### Stateless Connections
- "API" - For REST APIs using requests driver
- "MYSQL" - For MySQL Databases using aiomysql driver
- "SQLITE" - For SQLite Databases using aiosqlite driver
- "POSTGRESQL" - For PostgreSQL Databases using asyncpg driver
- "MONGODB" - For MongoDB Databases using motor driver
- "UNQLITE" - For UnQLite Databases using unqlite+asyncio driver

## Next Steps: 

Next steps involve extending the support for new communication technologies.
- "FILE" - For File operations using aiofiles driver
- "WEBSOCKET" - For WebSocket connections using websockets driver
- "MQTT" - For MQTT connections using asyncio-mqtt driver
- "REDIS" - For Redis Databases using aioredis driver
- "CASSANDRA" - For Cassandra Databases using cassandra-driver with asyncio support