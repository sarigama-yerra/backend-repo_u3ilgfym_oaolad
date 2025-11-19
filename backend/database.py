import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "moodica")

_client: Optional[MongoClient] = None
_db = None

try:
    _client = MongoClient(DATABASE_URL)
    _db = _client[DATABASE_NAME]
except Exception as e:
    _client = None
    _db = None


def db():
    return _db


def _collection(name: str) -> Collection:
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    doc = {**data, "created_at": now, "updated_at": now}
    col = _collection(collection_name)
    res = col.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    col = _collection(collection_name)
    cursor = col.find(filter_dict or {}).sort("created_at", -1).limit(limit)
    out: List[Dict[str, Any]] = []
    for d in cursor:
        d["_id"] = str(d.get("_id"))
        out.append(d)
    return out
