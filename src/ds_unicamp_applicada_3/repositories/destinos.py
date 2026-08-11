"""CRUD de destinos no Supabase."""

from __future__ import annotations

from ds_unicamp_applicada_3.database import get_supabase_client


def criar_destino(nome: str, pais: str, preco: float) -> dict:
    """Insere um novo destino e retorna o registro criado."""
    client = get_supabase_client()
    response = (
        client.table("destinos")
        .insert({"nome": nome, "pais": pais, "preco": preco})
        .execute()
    )
    return response.data[0]


def listar_destinos() -> list[dict]:
    """Retorna todos os destinos cadastrados."""
    client = get_supabase_client()
    response = client.table("destinos").select("*").execute()
    return response.data


def atualizar_destino(id: int, nome: str, pais: str, preco: float) -> dict:
    """Atualiza um destino existente e retorna o registro atualizado."""
    client = get_supabase_client()
    response = (
        client.table("destinos")
        .update({"nome": nome, "pais": pais, "preco": preco})
        .eq("id", id)
        .execute()
    )
    return response.data[0]


def excluir_destino(id: int) -> None:
    """Remove definitivamente um destino pelo ID."""
    client = get_supabase_client()
    client.table("destinos").delete().eq("id", id).execute()
