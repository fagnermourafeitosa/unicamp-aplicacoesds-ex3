"""CRUD de clientes no Supabase."""

from __future__ import annotations

from ds_unicamp_applicada_3.database import get_supabase_client


def criar_cliente(nome: str, email: str) -> dict:
    """Insere um novo cliente e retorna o registro criado."""
    client = get_supabase_client()
    response = client.table("clientes").insert({"nome": nome, "email": email}).execute()
    return response.data[0]


def listar_clientes() -> list[dict]:
    """Retorna todos os clientes cadastrados."""
    client = get_supabase_client()
    response = client.table("clientes").select("*").order("id", desc=True).execute()
    return response.data


def atualizar_cliente(id: int, nome: str, email: str) -> dict:
    """Atualiza nome e email de um cliente existente e retorna o registro atualizado."""
    client = get_supabase_client()
    response = (
        client.table("clientes")
        .update({"nome": nome, "email": email})
        .eq("id", id)
        .execute()
    )
    return response.data[0]


def excluir_cliente(id: int) -> None:
    """Remove definitivamente um cliente pelo ID."""
    client = get_supabase_client()
    client.table("clientes").delete().eq("id", id).execute()
