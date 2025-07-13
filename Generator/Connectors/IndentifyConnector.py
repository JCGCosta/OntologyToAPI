from Generator.Connectors.Stateful.SocketConnection import SocketConnection
from Generator.Connectors.Stateless.APIConnection import APIConnection
from Generator.Connectors.Stateless.MYSQLConnection import MySQLConnection
from Generator.Connectors.Stateless.MongoDBConnection import MongoDBConnection

SUPPORTED_CONNECTIONS = {
    "APICommunication": {
        "API": APIConnection,
    },
    "DatabaseCommunication": {
        "MYSQL": MySQLConnection,
        "MONGODB": MongoDBConnection,
    },

    "SocketConnection": {
        "Socket": SocketConnection,
    }
}

def identifyConnector(CommunicationType, CommunicationTechnology, args):
    try:
        connector_class = SUPPORTED_CONNECTIONS[CommunicationType][CommunicationTechnology]
        return connector_class(args)
    except KeyError as e:
        raise ValueError(f"Unsupported type or technology: {e}")