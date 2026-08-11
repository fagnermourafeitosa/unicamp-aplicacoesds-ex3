"""Create e Read de comentários no MongoDB."""

from __future__ import annotations

from datetime import datetime, timezone

from ds_unicamp_applicada_3.database import get_mongo_db

_COLLECTION = "comentarios"


def criar_comentario(cliente_id: int, destino_id: int, texto: str) -> dict:
    """Insere um comentário com data UTC automática e retorna o documento inserido."""
    db = get_mongo_db()
    doc = {
        "cliente_id": cliente_id,
        "destino_id": destino_id,
        "texto": texto,
        "data": datetime.now(tz=timezone.utc),
    }
    result = db[_COLLECTION].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


def listar_comentarios() -> list[dict]:
    """Retorna todos os comentários com data formatada como 'DD/MM/AAAA HH:MM'."""
    db = get_mongo_db()
    docs = list(db[_COLLECTION].find())
    result = []
    for doc in docs:
        data = doc.get("data")
        if isinstance(data, datetime):
            data_str = data.strftime("%d/%m/%Y %H:%M")
        else:
            data_str = str(data) if data else ""
        result.append(
            {
                "cliente_id": doc.get("cliente_id"),
                "destino_id": doc.get("destino_id"),
                "texto": doc.get("texto", ""),
                "data": data_str,
            }
        )
    return result
