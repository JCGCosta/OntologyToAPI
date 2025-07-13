from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, args):
        self.client = MongoClient(args["hasConnectionString"])
        self.db = self.client[connectionString.split('/')[-1]]

    def exec_query(self, collection: str, query: dict):
        collection = self.db[collection]
        return list(collection.find({}, query))