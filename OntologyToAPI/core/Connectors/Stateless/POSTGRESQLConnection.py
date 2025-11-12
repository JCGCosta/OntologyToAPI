from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime

async def datetime_handler(row, keys):
    return {
        key: (val.isoformat() if isinstance(val, datetime) else val)
        for key, val in zip(keys, row)
    }

class PostgreSQLConnection:
    def __init__(self, args):
        self.engine = create_async_engine(args["hasConnectionString"])

    async def exec_query(self, query: str):
        async with self.engine.connect() as connection:
            result = await connection.execute(text(query))
            rows = result.fetchall()
            keys = result.keys()
        return [await datetime_handler(row, keys) for row in rows]

    async def exec_insert(self, query: str):
        async with self.engine.begin() as connection:
            await connection.execute(text(query))
            result = await connection.execute(text("SELECT LAST_INSERT_ID() AS id"))
            row = result.fetchone()
            return row.id