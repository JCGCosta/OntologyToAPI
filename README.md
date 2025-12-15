# OntologyToAPI
> This python package is an ontology-driven API generator designed for 
> backend development by transforming structured domain 
> knowledge, different data sources and implemented business models into fully functional APIs. The tool accepts ontologies 
> specified in Turtle (.ttl), Resource Description Framework (.rdf)
> and Web Ontology Language (.owl).
>
> [![Publish to PyPI and TestPyPI](https://github.com/JCGCosta/OntologyToAPI/actions/workflows/python-publish.yml/badge.svg)](https://github.com/JCGCosta/OntologyToAPI/actions/workflows/python-publish.yml)

---

- A full documentation on how to extend your own ontologies using the OntologyToAPI framework is still in development, but you can check a small sample and docs at https://github.com/JCGCosta/OntologyToAPI/wiki

### Expected Results from a simple ontology specification

<img src="https://github.com/JCGCosta/OntologyToAPI/blob/master/example/APIEndpoints.png?raw=true" alt="APIEndpoints" title="APIEndpoints.">

### Supported communication technologies are (Currently):

#### Stateful Connections
- "SOCKET" - For Socket connections using asyncio streams

#### Stateless Connections
- "API" - For REST APIs using requests driver
- "MYSQL" - For MySQL Databases using aiomysql driver
- "SQLITE" - For SQLite Databases using aiosqlite driver
- "POSTGRESQL" - For PostgreSQL Databases using asyncpg driver
- "MONGODB" - For MongoDB Databases using motor driver
- "UNQLITE" - For UnQLite Databases using unqlite+asyncio driver

### Next Steps: 

Next steps involve extending the support for new communication technologies.
- "FILE" - For File operations using aiofiles driver
- "WEBSOCKET" - For WebSocket connections using websockets driver
- "MQTT" - For MQTT connections using asyncio-mqtt driver
- "REDIS" - For Redis Databases using aioredis driver
- "CASSANDRA" - For Cassandra Databases using cassandra-driver with asyncio support