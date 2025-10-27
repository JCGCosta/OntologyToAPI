import asyncio
from pymongo import AsyncMongoClient
import json, logging

class MongoDBConnection:
    def __init__(self, args):
        connString = args["hasConnectionString"].split('/')
        try:
            self.client = AsyncMongoClient("/".join(connString[:-1]))
        except:
            raise(Exception("Could not connect to MongoDB with the provided connection string"))
        self.db = self.client[connString[-1]]

    async def exec_query(self, collection_query: str):
        query_info = collection_query.split(".")
        collection = self.db[query_info[0]]
        query = json.loads(query_info[1])
        cursor = collection.find({}, query)
        results = await cursor.to_list()
        if not results: return []
        if "_id" in results[0].keys():
            for i in results:
                i["_id"] = str(i["_id"])
        return results
