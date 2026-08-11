"""Aplicação web Gradio — Agência de Viagens (DB Relacional + NoSQL)."""

from __future__ import annotations

from datetime import date
from uuid import uuid4
import gradio as gr
import pandas as pd

from ds_unicamp_applicada_3.repositories import clientes as repo_cli
from ds_unicamp_applicada_3.repositories import destinos as repo_dst
from ds_unicamp_applicada_3.repositories import vendas as repo_ven
from ds_unicamp_applicada_3.repositories import comentarios as repo_com


# ──────────────────────────────────────────────────────────────────
# Data helpers & Formatters
# ──────────────────────────────────────────────────────────────────

def _get_clientes_choices() -> list[str]:
    try:
        items = repo_cli.listar_clientes()
        return [f"{c['id']} – {c['nome']} ({c['email']})" for c in items]
    except Exception:
        return []


def _get_destinos_choices() -> list[str]:
    try:
        items = repo_dst.listar_destinos()
        return [
            f"{d['id']} – {d['nome']} - {d['pais']} (R$ {float(d.get('preco', 0)):.2f})"
            for d in items
        ]
    except Exception:
        return []


def _extract_id(choice: str | None) -> int | None:
    if not choice:
        return None
    try:
        return int(choice.split(" – ")[0].strip())
    except (ValueError, IndexError):
        return None


def _load_clientes_df() -> pd.DataFrame:
    try:
        items = repo_cli.listar_clientes()
        if not items:
            return pd.DataFrame(columns=["ID", "Nome", "E-mail"])
        return pd.DataFrame([{"ID": c["id"], "Nome": c["nome"], "E-mail": c["email"]} for c in items])
    except Exception as exc:
        print(f"Erro ao listar clientes: {exc}")
        return pd.DataFrame(columns=["ID", "Nome", "E-mail"])


def _load_destinos_df() -> pd.DataFrame:
    try:
        items = repo_dst.listar_destinos()
        if not items:
            return pd.DataFrame(columns=["ID", "Destino", "País", "Preço"])
        return pd.DataFrame([
            {
                "ID": d["id"],
                "Destino": d["nome"],
                "País": d["pais"],
                "Preço": f"R$ {float(d.get('preco', 0)):.2f}",
            }
            for d in items
        ])
    except Exception as exc:
        print(f"Erro ao listar destinos: {exc}")
        return pd.DataFrame(columns=["ID", "Destino", "País", "Preço"])


def _load_vendas_df() -> pd.DataFrame:
    try:
        items = repo_ven.listar_vendas()
        if not items:
            return pd.DataFrame(columns=["ID", "Cliente", "Destino", "Data da Viagem"])
        return pd.DataFrame([
            {
                "ID": v["id"],
                "Cliente": v.get("nome_cliente", ""),
                "Destino": v.get("nome_destino", ""),
                "Data da Viagem": v.get("data_viagem", ""),
            }
            for v in items
        ])
    except Exception as exc:
        print(f"Erro ao listar vendas: {exc}")
        return pd.DataFrame(columns=["ID", "Cliente", "Destino", "Data da Viagem"])


def _load_comentarios_df() -> pd.DataFrame:
    try:
        comentarios = repo_com.listar_comentarios()
        if not comentarios:
            return pd.DataFrame(columns=["Data/Hora", "Cliente", "Destino", "Comentário"])
        clientes_map = {c["id"]: c["nome"] for c in repo_cli.listar_clientes()}
        destinos_map = {d["id"]: f"{d['nome']} ({d['pais']})" for d in repo_dst.listar_destinos()}
        rows = []
        for c in comentarios:
            cli_nome = clientes_map.get(c["cliente_id"], f"Cliente #{c['cliente_id']}")
            dst_nome = destinos_map.get(c["destino_id"], f"Destino #{c['destino_id']}")
            rows.append({
                "Data/Hora": c.get("data", ""),
                "Cliente": cli_nome,
                "Destino": dst_nome,
                "Comentário": c.get("texto", ""),
            })
        return pd.DataFrame(rows)
    except Exception as exc:
        print(f"Erro ao listar comentários: {exc}")
        return pd.DataFrame(columns=["Data/Hora", "Cliente", "Destino", "Comentário"])


def _update_dataframe(dataframe: pd.DataFrame) -> gr.Dataframe:
    """Reconstrói a tabela com a quantidade correta de linhas após cada cadastro."""
    return gr.Dataframe(
        value=dataframe,
        headers=list(dataframe.columns),
        row_count=(max(len(dataframe.index), 1), "fixed"),
        interactive=False,
        wrap=True,
        key=f"table-{uuid4().hex}",
    )


# ──────────────────────────────────────────────────────────────────
# Actions / Callbacks
# ──────────────────────────────────────────────────────────────────

def handle_cadastrar_cliente(nome: str, email: str):
    if not nome or not nome.strip():
        gr.Warning("Por favor, informe o nome do cliente.")
        return "", "", _update_dataframe(_load_clientes_df())
    if not email or not email.strip():
        gr.Warning("Por favor, informe o e-mail do cliente.")
        return nome, "", _update_dataframe(_load_clientes_df())

    try:
        novo = repo_cli.criar_cliente(nome.strip(), email.strip())
        gr.Info(f"Cliente '{novo.get('nome', nome.strip())}' (ID #{novo.get('id')}) cadastrado com sucesso!")
        return "", "", _update_dataframe(_load_clientes_df())
    except Exception as exc:
        gr.Error(f"Erro ao cadastrar cliente: {exc}")
        return nome, email, _update_dataframe(_load_clientes_df())


def handle_cadastrar_destino(nome: str, pais: str, preco: float | None):
    if not nome or not nome.strip():
        gr.Warning("Por favor, informe o nome do destino.")
        return "", "", preco, _update_dataframe(_load_destinos_df())
    if not pais or not pais.strip():
        gr.Warning("Por favor, informe o país.")
        return nome, "", preco, _update_dataframe(_load_destinos_df())
    if preco is None or preco < 0:
        gr.Warning("Informe um preço válido (maior ou igual a 0).")
        return nome, pais, 0.0, _update_dataframe(_load_destinos_df())

    try:
        novo = repo_dst.criar_destino(nome.strip(), pais.strip(), float(preco))
        gr.Info(f"Destino '{novo.get('nome', nome.strip())}' (ID #{novo.get('id')}) cadastrado com sucesso!")
        return "", "", 0.0, _update_dataframe(_load_destinos_df())
    except Exception as exc:
        gr.Error(f"Erro ao cadastrar destino: {exc}")
        return nome, pais, preco, _update_dataframe(_load_destinos_df())


def handle_registrar_venda(cliente_choice: str | None, destino_choice: str | None, data_viagem: str):
    cli_id = _extract_id(cliente_choice)
    dst_id = _extract_id(destino_choice)
    if not cli_id:
        gr.Warning("Selecione um cliente para a venda.")
        return _update_dataframe(_load_vendas_df())
    if not dst_id:
        gr.Warning("Selecione um destino para a venda.")
        return _update_dataframe(_load_vendas_df())
    if not data_viagem or not data_viagem.strip():
        gr.Warning("Informe a data da viagem.")
        return _update_dataframe(_load_vendas_df())

    try:
        nova = repo_ven.criar_venda(cli_id, dst_id, data_viagem.strip())
        gr.Info(f"Venda (ID #{nova.get('id')}) registrada com sucesso!")
        return _update_dataframe(_load_vendas_df())
    except Exception as exc:
        gr.Error(f"Erro ao registrar venda: {exc}")
        return _update_dataframe(_load_vendas_df())


def handle_enviar_comentario(cliente_choice: str | None, destino_choice: str | None, texto: str):
    cli_id = _extract_id(cliente_choice)
    dst_id = _extract_id(destino_choice)
    if not cli_id:
        gr.Warning("Selecione quem está avaliando.")
        return texto, _update_dataframe(_load_comentarios_df())
    if not dst_id:
        gr.Warning("Selecione o destino avaliado.")
        return texto, _update_dataframe(_load_comentarios_df())
    if not texto or not texto.strip():
        gr.Warning("Digite o texto do seu comentário.")
        return texto, _update_dataframe(_load_comentarios_df())

    try:
        repo_com.criar_comentario(cli_id, dst_id, texto.strip())
        gr.Info("Comentário salvo com sucesso!")
        return "", _update_dataframe(_load_comentarios_df())
    except Exception as exc:
        gr.Error(f"Erro ao salvar comentário: {exc}")
        return texto, _update_dataframe(_load_comentarios_df())


def refresh_vendas_tab():
    return gr.Dropdown(choices=_get_clientes_choices()), gr.Dropdown(choices=_get_destinos_choices()), _load_vendas_df()


def refresh_comentarios_tab():
    return gr.Dropdown(choices=_get_clientes_choices()), gr.Dropdown(choices=_get_destinos_choices()), _load_comentarios_df()


# ──────────────────────────────────────────────────────────────────
# UI Layout
# ──────────────────────────────────────────────────────────────────

theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="slate",
    neutral_hue="slate",
)

with gr.Blocks(title="Agência de Viagens — Portal Web") as demo:

    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
                # ✈️ Agência de Viagens
                **Portal Unificado de Cadastro e Avaliações** · *DB Relacional + NoSQL*
                """
            )

    with gr.Tabs() as tabs:

        # ────────────── TAB 1: CLIENTES ──────────────
        with gr.Tab("👤 Clientes", id="tab_clientes"):
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### ➕ Novo Cliente")
                        cli_nome = gr.Textbox(
                            label="Nome Completo",
                            placeholder="ex: Maria Eduarda Silva",
                        )
                        cli_email = gr.Textbox(
                            label="E-mail",
                            placeholder="ex: maria@email.com",
                        )
                        btn_cad_cli = gr.Button("Cadastrar Cliente", variant="primary")

                with gr.Column(scale=2):
                    with gr.Group():
                        with gr.Row():
                            gr.Markdown("### 📋 Clientes Cadastrados (DB Relacional)")
                            btn_refresh_cli = gr.Button("🔄 Atualizar", size="sm", variant="secondary")
                        cli_table = gr.Dataframe(
                            headers=["ID", "Nome", "E-mail"],
                            value=_load_clientes_df,
                            wrap=True,
                        )

        # ────────────── TAB 2: DESTINOS ──────────────
        with gr.Tab("📍 Destinos", id="tab_destinos"):
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### ➕ Novo Destino")
                        dst_nome = gr.Textbox(
                            label="Destino / Cidade",
                            placeholder="ex: Fernando de Noronha",
                        )
                        dst_pais = gr.Textbox(
                            label="País",
                            placeholder="ex: Brasil",
                        )
                        dst_preco = gr.Number(
                            label="Preço do Pacote (R$)",
                            minimum=0,
                            precision=2,
                            value=1500.0,
                        )
                        btn_cad_dst = gr.Button("Cadastrar Destino", variant="primary")

                with gr.Column(scale=2):
                    with gr.Group():
                        with gr.Row():
                            gr.Markdown("### 📋 Destinos Cadastrados (DB Relacional)")
                            btn_refresh_dst = gr.Button("🔄 Atualizar", size="sm", variant="secondary")
                        dst_table = gr.Dataframe(
                            headers=["ID", "Destino", "País", "Preço"],
                            value=_load_destinos_df,
                            wrap=True,
                        )

        # ────────────── TAB 3: VENDAS ──────────────
        with gr.Tab("🎫 Vendas", id="tab_vendas") as tab_vendas:
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### ➕ Registrar Nova Venda")
                        ven_cli_dropdown = gr.Dropdown(
                            label="Selecione o Cliente",
                            choices=_get_clientes_choices(),
                            interactive=True,
                        )
                        ven_dst_dropdown = gr.Dropdown(
                            label="Selecione o Destino",
                            choices=_get_destinos_choices(),
                            interactive=True,
                        )
                        ven_data = gr.Textbox(
                            label="Data da Viagem (AAAA-MM-DD)",
                            value=date.today().isoformat(),
                            placeholder="ex: 2026-12-25",
                        )
                        btn_cad_ven = gr.Button("Registrar Venda", variant="primary")

                with gr.Column(scale=2):
                    with gr.Group():
                        with gr.Row():
                            gr.Markdown("### 📋 Histórico de Vendas (DB Relacional)")
                            btn_refresh_ven = gr.Button("🔄 Atualizar", size="sm", variant="secondary")
                        ven_table = gr.Dataframe(
                            headers=["ID", "Cliente", "Destino", "Data da Viagem"],
                            value=_load_vendas_df,
                            wrap=True,
                        )

        # ────────────── TAB 4: COMENTÁRIOS ──────────────
        with gr.Tab("💬 Avaliações (NoSQL)", id="tab_comentarios") as tab_comentarios:
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### ✍️ Enviar Avaliação de Viagem")
                        com_cli_dropdown = gr.Dropdown(
                            label="Viajante",
                            choices=_get_clientes_choices(),
                            interactive=True,
                        )
                        com_dst_dropdown = gr.Dropdown(
                            label="Destino Avaliado",
                            choices=_get_destinos_choices(),
                            interactive=True,
                        )
                        com_texto = gr.Textbox(
                            label="Comentário sobre a experiência",
                            placeholder="Conte os pontos fortes da viagem, hospedagem, passeios...",
                            lines=4,
                        )
                        btn_cad_com = gr.Button("Salvar Avaliação", variant="primary")

                with gr.Column(scale=2):
                    with gr.Group():
                        with gr.Row():
                            gr.Markdown("### 💬 Mural de Avaliações (NoSQL)")
                            btn_refresh_com = gr.Button("🔄 Atualizar", size="sm", variant="secondary")
                        com_table = gr.Dataframe(
                            headers=["Data/Hora", "Cliente", "Destino", "Comentário"],
                            value=_load_comentarios_df,
                            wrap=True,
                        )

    # ──────────────────────────────────────────────────────────────
    # Event Bindings
    # ──────────────────────────────────────────────────────────────

    # Cadastrar Cliente
    btn_cad_cli.click(
        fn=handle_cadastrar_cliente,
        inputs=[cli_nome, cli_email],
        outputs=[cli_nome, cli_email, cli_table],
    )
    btn_refresh_cli.click(fn=_load_clientes_df, outputs=[cli_table])

    # Cadastrar Destino
    btn_cad_dst.click(
        fn=handle_cadastrar_destino,
        inputs=[dst_nome, dst_pais, dst_preco],
        outputs=[dst_nome, dst_pais, dst_preco, dst_table],
    )
    btn_refresh_dst.click(fn=_load_destinos_df, outputs=[dst_table])

    # Registrar Venda
    btn_cad_ven.click(
        fn=handle_registrar_venda,
        inputs=[ven_cli_dropdown, ven_dst_dropdown, ven_data],
        outputs=[ven_table],
    )
    btn_refresh_ven.click(fn=_load_vendas_df, outputs=[ven_table])

    # Enviar Comentário
    btn_cad_com.click(
        fn=handle_enviar_comentario,
        inputs=[com_cli_dropdown, com_dst_dropdown, com_texto],
        outputs=[com_texto, com_table],
    )
    btn_refresh_com.click(fn=_load_comentarios_df, outputs=[com_table])

    # Tab selection auto-refresh
    tab_vendas.select(
        fn=refresh_vendas_tab,
        outputs=[ven_cli_dropdown, ven_dst_dropdown, ven_table],
    )
    tab_comentarios.select(
        fn=refresh_comentarios_tab,
        outputs=[com_cli_dropdown, com_dst_dropdown, com_table],
    )


if __name__ == "__main__":
    demo.launch(theme=theme)
