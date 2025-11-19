import asyncio
import json
import logging
from urllib.parse import urlparse, unquote
from typing import Any, Dict, List, Optional
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

    async def exec_query(self, collection_query: str) -> List[Any]:
        collection, filt, projection = self._parse_collection_query(collection_query)
        docs = await asyncio.to_thread(self._get_collection_docs, collection)
        filtered = self._filter_docs(docs, filt)
        if projection is not None:
            return self._project_docs(filtered, projection)
        return filtered

    # ---------- internals (sync) ----------

    def _parse_collection_query(
        self, collection_query: str
    ) -> (str, Dict[str, Any], Optional[Dict[str, int]]):
        try:
            collection, json_str = collection_query.split(".", 1)
            spec = json.loads(json_str)
            if not isinstance(spec, dict):
                raise ValueError("JSON must be an object.")

            # Detect projection-only spec: { field1: 1, field2: 0, ... }
            is_projection = all(
                not isinstance(v, dict) and v in (0, 1)
                for v in spec.values()
            )

            if is_projection:
                # No filter, only projection
                return collection, {}, spec
            else:
                # Filter only, no projection
                return collection, spec, None

        except Exception as e:
            raise ValueError(
                f"Invalid collection_query format; expected 'collection.{{...}}'. Error: {e}"
            )

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
        if not filt:
            return docs

        def match(doc: Dict[str, Any]) -> bool:
            for key, cond in filt.items():
                val = doc.get(key, None)
                if isinstance(cond, dict):
                    for op, rhs in cond.items():
                        if op == "$gt" and not (val is not None and val > rhs):
                            return False
                        if op == "$lt" and not (val is not None and val < rhs):
                            return False
                        if op == "$eq" and not (val == rhs):
                            return False
                        # extend here with $gte, $lte, $ne, $in, etc.
                else:
                    if val != cond:
                        return False
            return True

        return [d for d in docs if match(d)]

    def _project_docs(self, docs: List[Dict[str, Any]], projection: Dict[str, int]) -> List[Any]:

        include_fields = {k for k, v in projection.items() if v == 1}
        exclude_fields = {k for k, v in projection.items() if v == 0}

        include_no_id = {k for k in include_fields if k != "id"}
        exclude_no_id = {k for k in exclude_fields if k != "id"}

        if include_no_id and exclude_no_id:
            raise ValueError("Cannot mix inclusion and exclusion in projection (except for id).")

        # ---------- SINGLE FIELD SPECIAL CASE ----------
        if len(include_no_id) == 1 and not exclude_no_id and "id" not in exclude_fields:
            field = next(iter(include_no_id))
            result: List[Any] = []

            for doc in docs:
                if "id" not in doc or field not in doc:
                    continue

                doc_id = str(doc["id"])  # ensure JSON-safe key
                value = doc[field]
                result.append({doc_id: value})

            return result

        # ---------- GENERAL CASE ----------
        result: List[Any] = []

        for doc in docs:
            if include_no_id:
                projected = {
                    k: doc.get(k)
                    for k in include_fields
                    if k in doc
                }
            else:
                projected = {
                    k: v
                    for k, v in doc.items()
                    if k not in exclude_no_id
                }

            # Explicit id exclusion
            if "id" in exclude_fields:
                projected.pop("id", None)
            else:
                # Preserve id if present
                if "id" in doc:
                    projected["id"] = doc["id"]

            result.append(projected)

        return result

