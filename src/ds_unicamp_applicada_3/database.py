"""Singleton de conexões com Supabase e MongoDB."""

from __future__ import annotations

from supabase import Client, create_client
from pymongo import MongoClient
from pymongo.database import Database

from ds_unicamp_applicada_3.config import SUPABASE_URL, SUPABASE_KEY, MONGODB_URI, MONGODB_DB_NAME

_supabase_client: Client | None = None
_mongo_client: MongoClient | None = None


def get_supabase_client() -> Client:
    """Retorna o cliente Supabase singleton."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def get_mongo_db() -> Database:
    """Retorna o banco MongoDB singleton (agencia_viagens)."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(MONGODB_URI)
    return _mongo_client[MONGODB_DB_NAME]
