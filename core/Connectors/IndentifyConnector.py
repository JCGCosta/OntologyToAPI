from core.Connectors.Stateful.SocketConnection import SocketConnection
from core.Connectors.Stateless.APIConnection import APIConnection
from core.Connectors.Stateless.MYSQLConnection import MySQLConnection
from core.Connectors.Stateless.MongoDBConnection import MongoDBConnection

SUPPORTED_CONNECTIONS = {
    "API": APIConnection,
    "MYSQL": MySQLConnection,
    "MONGODB": MongoDBConnection,
    "Socket": SocketConnection
}

def identifyConnector(CommunicationTechnology, args):
    try:
        connector_class = SUPPORTED_CONNECTIONS[str(CommunicationTechnology)]
        return connector_class(args)
    except KeyError as e:
        raise ValueError(f"Unsupported type or technology: {e}")