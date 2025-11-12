from OntologyToAPI.core.Connectors.Stateful.SocketConnection import SocketConnection
from OntologyToAPI.core.Connectors.Stateless.APIConnection import APIConnection
from OntologyToAPI.core.Connectors.Stateless.MYSQLConnection import MySQLConnection
from OntologyToAPI.core.Connectors.Stateless.MongoDBConnection import MongoDBConnection
from OntologyToAPI.core.Connectors.Stateless.SQLITEConnection import SQLiteConnection
from OntologyToAPI.core.Connectors.Stateless.POSTGRESQLConnection import PostgreSQLConnection
from OntologyToAPI.core.Connectors.Stateless.UNQLITEConnection import UnQLiteConnection

SUPPORTED_CONNECTIONS = {
    "API": APIConnection,
    "SOCKET": SocketConnection,

    # SQL Databases
    "MYSQL": MySQLConnection,
    "SQLITE": SQLiteConnection,
    "POSTGRESQL": PostgreSQLConnection,

    # NoSQL Databases
    "MONGODB": MongoDBConnection,
    "UNQLITE": UnQLiteConnection
}

def identifyConnector(CommunicationTechnology, args):
    try:
        connector_class = SUPPORTED_CONNECTIONS[str(CommunicationTechnology)]
        return connector_class(args)
    except KeyError as e:
        raise ValueError(f"Unsupported type or technology: {e} please check the Ontology.")