import asyncio
import json
import logging
from urllib.parse import urlparse, unquote
from typing import Any, Dict, List
from unqlite import UnQLite

class UnQLiteConnection:
    def __init__(self, args: Dict[str, str]):
        raw = args.get("hasConnectionString")
        if not raw:
            raise ValueError("Missing 'hasConnectionString' in args.")
        parsed = urlparse(raw)

        if parsed.scheme not in ("unqlite+asyncio",):
            raise ValueError(f"Unsupported scheme: {parsed.scheme}. Use 'unqlite+asyncio'.")

        path = unquote(parsed.netloc or "")
        if not path:
            raise ValueError(f"Empty database path in connection string.")
        if path == "/:memory:":
            db_path = ":memory:"
        else:
            db_path = path

        try:
            self._db = UnQLite(db_path)
        except Exception as e:
            raise Exception(f"Could not open UnQLite database at '{db_path}': {e}")

    # ---------- public API ----------

    async def exec_query(self, collection_query: str) -> List[Dict[str, Any]]:
        collection, filt = self._parse_collection_query(collection_query)
        docs = await asyncio.to_thread(self._get_collection_docs, collection)
        return self._filter_docs(docs, filt)

    # ---------- internals (sync) ----------

    def _parse_collection_query(self, collection_query: str):
        try:
            collection, json_str = collection_query.split(".", 1)
            filt = json.loads(json_str)
            if not isinstance(filt, dict):
                raise ValueError("Filter JSON must be an object.")
            return collection, filt
        except Exception as e:
            raise ValueError(f"Invalid collection_query format; expected 'collection.{{...}}'. Error: {e}")

    def _get_collection_docs(self, collection: str) -> List[Dict[str, Any]]:
        try:
            if collection not in self._db:
                return []
            data = self._db[collection]
            if isinstance(data, (bytes, str)):
                data = json.loads(data)
            if isinstance(data, list):
                return [d for d in data if isinstance(d, dict)]
            if isinstance(data, dict):
                return [data]
            return []
        except Exception as e:
            logging.error(f"Error reading collection '{collection}': {e}")
            return []

    def _persist_collection(self, collection: str, docs: List[Dict[str, Any]]) -> None:
        try:
            self._db[collection] = json.dumps(docs, separators=(",", ":"))
        except Exception as e:
            logging.error(f"Error writing collection '{collection}': {e}")
            raise

    def _filter_docs(self, docs: List[Dict[str, Any]], filt: Dict[str, Any]) -> List[Dict[str, Any]]:
        def match(doc: Dict[str, Any]) -> bool:
            for key, cond in filt.items():
                val = doc.get(key, None)
                if isinstance(cond, dict):
                    for op, rhs in cond.items():
                        if op == "$gt" and not (val is not None and val > rhs): return False
                        if op == "$lt" and not (val is not None and val < rhs): return False
                        if op == "$eq" and not (val == rhs): return False
                        # extend here with $gte, $lte, $ne, $in, etc.
                else:
                    if val != cond:
                        return False
            return True
        return [d for d in docs if match(d)]