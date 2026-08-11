"""CRUD de vendas no Supabase, com resolução de nomes de cliente e destino."""

from __future__ import annotations

from ds_unicamp_applicada_3.database import get_supabase_client


def criar_venda(cliente_id: int, destino_id: int, data_viagem: str) -> dict:
    """Insere uma nova venda e retorna o registro criado."""
    client = get_supabase_client()
    response = (
        client.table("vendas")
        .insert(
            {
                "cliente_id": cliente_id,
                "destino_id": destino_id,
                "data_viagem": data_viagem,
            }
        )
        .execute()
    )
    return response.data[0]


def listar_vendas() -> list[dict]:
    """Retorna todas as vendas com nome_cliente e nome_destino já resolvidos."""
    client = get_supabase_client()
    response = (
        client.table("vendas")
        .select("id, data_viagem, clientes(nome), destinos(nome)")
        .order("id", desc=True)
        .execute()
    )
    result = []
    for row in response.data:
        result.append(
            {
                "id": row["id"],
                "cliente_id": row.get("cliente_id"),
                "destino_id": row.get("destino_id"),
                "nome_cliente": (row.get("clientes") or {}).get("nome", ""),
                "nome_destino": (row.get("destinos") or {}).get("nome", ""),
                "data_viagem": row["data_viagem"],
            }
        )
    return result


def atualizar_venda(id: int, cliente_id: int, destino_id: int, data_viagem: str) -> dict:
    """Atualiza uma venda existente e retorna o registro atualizado."""
    client = get_supabase_client()
    response = (
        client.table("vendas")
        .update(
            {
                "cliente_id": cliente_id,
                "destino_id": destino_id,
                "data_viagem": data_viagem,
            }
        )
        .eq("id", id)
        .execute()
    )
    return response.data[0]


def excluir_venda(id: int) -> None:
    """Remove definitivamente uma venda pelo ID."""
    client = get_supabase_client()
    client.table("vendas").delete().eq("id", id).execute()
