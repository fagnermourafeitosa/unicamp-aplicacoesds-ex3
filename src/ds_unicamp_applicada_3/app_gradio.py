"""Aplicação web Gradio — Agência de Viagens."""

from __future__ import annotations

import gradio as gr

from ds_unicamp_applicada_3.repositories import clientes as repo_cli
from ds_unicamp_applicada_3.repositories import destinos as repo_dst
from ds_unicamp_applicada_3.repositories import vendas as repo_ven
from ds_unicamp_applicada_3.repositories import comentarios as repo_com

# ──────────────────────────────────────────────────────────────────
# CSS customizado (paleta "cartão de embarque")
# ──────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:ital,wght@1,700&family=JetBrains+Mono&display=swap');

:root {
  --color-bg:        #0D1B2A;
  --color-panel:     #1B4965;
  --color-accent:    #5FA8D3;
  --color-text:      #CAE9FF;
  --color-cta:       #E9C46A;
  --color-cta-text:  #0D1B2A;
  --font-display:    'Playfair Display', Georgia, serif;
  --font-body:       'Inter', system-ui, sans-serif;
  --font-data:       'JetBrains Mono', 'Courier New', monospace;
  --radius-sm:       4px;
  --radius-md:       8px;
  --space-sm:        8px;
  --space-md:        16px;
  --space-lg:        32px;
}

body, .gradio-container {
  background-color: var(--color-bg) !important;
  font-family: var(--font-body) !important;
  color: var(--color-text) !important;
}

/* ── faixa topo ── */
#header-strip {
  background: var(--color-bg);
  padding: 24px 40px;
  text-align: center;
  letter-spacing: 4px;
  font-family: var(--font-display);
  font-style: italic;
  font-size: 1.5rem;
  color: var(--color-cta);
  border-bottom: 1px solid var(--color-panel);
  margin-bottom: 0;
}

/* ── abas ── */
.tabs > .tab-nav {
  background: var(--color-bg) !important;
  border-bottom: 1px solid var(--color-panel) !important;
}
.tabs > .tab-nav button {
  color: rgba(202,233,255,.6) !important;
  font-family: var(--font-body) !important;
  font-size: 0.95rem !important;
  padding: 10px 20px !important;
  border-bottom: 2px solid transparent !important;
}
.tabs > .tab-nav button.selected {
  color: var(--color-cta) !important;
  border-bottom: 2px solid var(--color-cta) !important;
}

/* ── painel de aba ── */
.tabitem {
  background: var(--color-panel) !important;
  border-radius: var(--radius-md) !important;
  padding: var(--space-lg) 40px !important;
}

/* ── labels & inputs ── */
label span, .label-wrap span {
  color: var(--color-text) !important;
  font-size: 13px !important;
  font-family: var(--font-body) !important;
}
input[type=text], input[type=number], textarea, select {
  background: var(--color-bg) !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-accent) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
}
input:focus, textarea:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px var(--color-accent) !important;
}

/* ── botão CTA âmbar ── */
button.primary, #btn-cad-cliente, #btn-cad-destino, #btn-reg-venda, #btn-enviar-com {
  background: var(--color-cta) !important;
  color: var(--color-cta-text) !important;
  font-weight: 700 !important;
  border-radius: var(--radius-sm) !important;
  border: none !important;
  width: 100% !important;
}
button.primary:hover {
  background: #d4b05a !important;
}

/* ── botão secundário ── */
button.secondary, #btn-ver-comentarios {
  background: transparent !important;
  color: var(--color-text) !important;
  border: 1px solid var(--color-accent) !important;
  border-radius: var(--radius-sm) !important;
}
button.secondary:hover {
  background: var(--color-accent) !important;
  color: var(--color-bg) !important;
}

/* ── status ── */
.status-ok  { color: var(--color-accent) !important; font-size: 14px !important; }
.status-err { color: var(--color-cta)    !important; font-size: 14px !important; }

/* ── tabela ── */
.gr-dataframe, .gr-dataframe table {
  background: var(--color-bg) !important;
  color: var(--color-text) !important;
  font-family: var(--font-data) !important;
  font-size: 13px !important;
}
.gr-dataframe thead th {
  background: var(--color-panel) !important;
  color: var(--color-cta) !important;
}

/* ── empty state ── */
#empty-state {
  font-family: var(--font-body);
  font-style: italic;
  color: rgba(202,233,255,.6);
  text-align: center;
  padding: 24px;
}
"""


# ──────────────────────────────────────────────────────────────────
# Helpers para popular dropdowns
# ──────────────────────────────────────────────────────────────────

def _choices_clientes() -> list[str]:
    return [f"{c['id']} – {c['nome']}" for c in repo_cli.listar_clientes()]


def _choices_destinos() -> list[str]:
    return [f"{d['id']} – {d['nome']} ({d['pais']})" for d in repo_dst.listar_destinos()]


def _extract_id(choice: str) -> int:
    """Extrai o ID numérico da string 'id – Nome'."""
    return int(choice.split(" – ")[0])


# ──────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────

def cb_criar_cliente(nome: str, email: str) -> str:
    try:
        repo_cli.criar_cliente(nome.strip(), email.strip())
        return "✓ Cliente cadastrado com sucesso."
    except Exception as exc:
        return f"✗ Erro: {exc}"


def cb_criar_destino(nome: str, pais: str, preco: float | None) -> str:
    try:
        repo_dst.criar_destino(nome.strip(), pais.strip(), float(preco or 0))
        return "✓ Destino cadastrado com sucesso."
    except Exception as exc:
        return f"✗ Erro: {exc}"


def cb_criar_venda(cliente_choice: str, destino_choice: str, data_viagem: str) -> str:
    try:
        cliente_id = _extract_id(cliente_choice)
        destino_id = _extract_id(destino_choice)
        repo_ven.criar_venda(cliente_id, destino_id, data_viagem.strip())
        nome_cli = cliente_choice.split(" – ", 1)[1] if " – " in cliente_choice else cliente_choice
        nome_dst = destino_choice.split(" – ", 1)[1] if " – " in destino_choice else destino_choice
        return f"✓ Venda registrada para {nome_cli} → {nome_dst}."
    except Exception as exc:
        return f"✗ Erro: cliente ou destino inválido. ({exc})"


def cb_criar_comentario(cliente_choice: str, destino_choice: str, texto: str) -> str:
    try:
        cliente_id = _extract_id(cliente_choice)
        destino_id = _extract_id(destino_choice)
        repo_com.criar_comentario(cliente_id, destino_id, texto.strip())
        return "✓ Comentário enviado com sucesso."
    except Exception as exc:
        return f"✗ Erro: {exc}"


def cb_listar_comentarios():
    comentarios = repo_com.listar_comentarios()
    if not comentarios:
        return []
    # Enriquecer com nomes via repositório de clientes/destinos
    clientes_map = {c["id"]: c["nome"] for c in repo_cli.listar_clientes()}
    destinos_map = {d["id"]: d["nome"] for d in repo_dst.listar_destinos()}
    rows = []
    for c in comentarios:
        rows.append(
            {
                "Cliente": clientes_map.get(c["cliente_id"], str(c["cliente_id"])),
                "Destino": destinos_map.get(c["destino_id"], str(c["destino_id"])),
                "Comentário": c["texto"],
                "Data": c["data"],
            }
        )
    return rows


# ──────────────────────────────────────────────────────────────────
# Interface
# ──────────────────────────────────────────────────────────────────

with gr.Blocks(css=CUSTOM_CSS, title="Agência de Viagens") as demo:

    # ── Faixa topo ──
    gr.HTML('<div id="header-strip">FROM: VOCÊ &nbsp;✈&nbsp; TO: QUALQUER LUGAR</div>')

    with gr.Tabs():

        # ────────────── ABA CLIENTES ──────────────
        with gr.Tab("Clientes"):
            with gr.Row():
                with gr.Column(scale=4):
                    cli_nome  = gr.Textbox(label="Nome do viajante",   placeholder="ex: Maria Silva")
                    cli_email = gr.Textbox(label="E-mail de contato",  placeholder="ex: maria@email.com")
                    btn_cli   = gr.Button("Cadastrar Cliente", variant="primary", elem_id="btn-cad-cliente")
                with gr.Column(scale=6):
                    cli_status = gr.Textbox(label="Status", interactive=False, show_label=False)

            btn_cli.click(cb_criar_cliente, inputs=[cli_nome, cli_email], outputs=cli_status)

        # ────────────── ABA DESTINOS ──────────────
        with gr.Tab("Destinos"):
            with gr.Row():
                with gr.Column(scale=4):
                    dst_nome  = gr.Textbox(label="Nome do destino", placeholder="ex: Lisboa")
                    dst_pais  = gr.Textbox(label="País",            placeholder="ex: Portugal")
                    dst_preco = gr.Number( label="Preço (R$)",      minimum=0, precision=2)
                    btn_dst   = gr.Button("Cadastrar Destino", variant="primary", elem_id="btn-cad-destino")
                with gr.Column(scale=6):
                    dst_status = gr.Textbox(label="Status", interactive=False, show_label=False)

            btn_dst.click(cb_criar_destino, inputs=[dst_nome, dst_pais, dst_preco], outputs=dst_status)

        # ────────────── ABA VENDAS ──────────────
        with gr.Tab("Vendas"):
            with gr.Row():
                with gr.Column(scale=4):
                    ven_cliente = gr.Dropdown(
                        label="Cliente",
                        choices=_choices_clientes(),
                        allow_custom_value=False,
                    )
                    ven_destino = gr.Dropdown(
                        label="Destino",
                        choices=_choices_destinos(),
                        allow_custom_value=False,
                    )
                    ven_data = gr.Textbox(label="Data da viagem", placeholder="AAAA-MM-DD")
                    btn_ven  = gr.Button("Registrar Venda", variant="primary", elem_id="btn-reg-venda")
                with gr.Column(scale=6):
                    ven_status = gr.Textbox(label="Status", interactive=False, show_label=False)

            btn_ven.click(cb_criar_venda, inputs=[ven_cliente, ven_destino, ven_data], outputs=ven_status)

        # ────────────── ABA COMENTÁRIOS ──────────────
        with gr.Tab("Comentários"):
            with gr.Row():
                with gr.Column(scale=4):
                    com_cliente = gr.Dropdown(
                        label="Quem está avaliando?",
                        choices=_choices_clientes(),
                        allow_custom_value=False,
                    )
                    com_destino = gr.Dropdown(
                        label="Destino visitado",
                        choices=_choices_destinos(),
                        allow_custom_value=False,
                    )
                    com_texto  = gr.Textbox(
                        label="Sua avaliação",
                        lines=4,
                        max_lines=8,
                        placeholder="Conte como foi a viagem...",
                    )
                    btn_com    = gr.Button("Enviar Comentário", variant="primary", elem_id="btn-enviar-com")
                    com_status = gr.Textbox(label="Status", interactive=False, show_label=False)

                with gr.Column(scale=6):
                    btn_ver = gr.Button("Ver Todos os Comentários", variant="secondary", elem_id="btn-ver-comentarios")
                    com_tabela = gr.Dataframe(
                        headers=["Cliente", "Destino", "Comentário", "Data"],
                        datatype=["str", "str", "str", "str"],
                        interactive=False,
                        label="Comentários",
                    )

            btn_com.click(cb_criar_comentario, inputs=[com_cliente, com_destino, com_texto], outputs=com_status)
            btn_ver.click(cb_listar_comentarios, inputs=[], outputs=com_tabela)


if __name__ == "__main__":
    demo.launch()
