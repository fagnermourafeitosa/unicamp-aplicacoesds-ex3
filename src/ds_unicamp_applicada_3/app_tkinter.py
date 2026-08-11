"""Interface desktop de administração — Agência de Viagens (Tkinter CRUD)."""

from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from ds_unicamp_applicada_3.repositories import clientes as repo_cli
from ds_unicamp_applicada_3.repositories import destinos as repo_dst
from ds_unicamp_applicada_3.repositories import vendas as repo_ven

# ──────────────────────────────────────────────────────────────────
# Paleta alinhada à interface Gradio em modo escuro
# ──────────────────────────────────────────────────────────────────
BG        = "#0A0E1D"
PANEL     = "#1E293A"
SURFACE   = "#344154"
SURFACE_HOVER = "#485568"
ACCENT    = "#0795D2"
TEXT      = "#F4F6FA"
MUTED     = "#93A1B5"
DANGER    = "#C9495E"
WHITE     = "#FFFFFF"


def _apply_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame",            background=PANEL)
    style.configure("TNotebook",         background=BG,    borderwidth=0)
    style.configure("TNotebook.Tab",     background=BG,    foreground=TEXT,
                                         padding=[16, 9],  font=("Inter", 12))
    style.map("TNotebook.Tab",           background=[("selected", BG)],
                                         foreground=[("selected", ACCENT)])

    style.configure("TLabel",            background=PANEL, foreground=TEXT,
                                         font=("Inter", 11))
    style.configure("Header.TLabel",     background=BG,    foreground=TEXT,
                                         font=("Inter", 20, "bold"))
    style.configure("Status.TLabel",     background=PANEL, foreground=ACCENT,
                                         font=("Inter", 11, "italic"))
    style.configure("StatusErr.TLabel",  background=PANEL, foreground="#FFB4BF",
                                         font=("Inter", 11, "italic"))

    style.configure("TEntry",            fieldbackground=SURFACE, foreground=TEXT,
                                         insertcolor=TEXT,   bordercolor=SURFACE,
                                         relief="flat")
    style.configure("TCombobox",         fieldbackground=SURFACE, foreground=TEXT,
                                         selectbackground=ACCENT, arrowcolor=TEXT)

    style.configure("Primary.TButton",   background=ACCENT, foreground=WHITE,
                                         font=("Inter", 11, "bold"), relief="flat",
                                         padding=[10, 8])
    style.map("Primary.TButton",         background=[("active", "#0AA7EA")])

    style.configure("Secondary.TButton", background=SURFACE_HOVER, foreground=TEXT,
                                         font=("Inter", 11), relief="flat",
                                         padding=[10, 8])
    style.map("Secondary.TButton",       background=[("active", "#5A687B")])

    style.configure("Danger.TButton",    background=DANGER, foreground=WHITE,
                                         font=("Inter", 11, "bold"), relief="flat",
                                         padding=[8, 6])
    style.map("Danger.TButton",          background=[("active", "#AE3B4E")])

    style.configure("Treeview",          background="#0F1629", foreground=TEXT,
                                         fieldbackground="#0F1629", rowheight=34,
                                         font=("JetBrains Mono", 11), borderwidth=0)
    style.configure("Treeview.Heading",  background="#0F1629", foreground=TEXT,
                                         font=("Inter", 11, "bold"), relief="flat")
    style.map("Treeview",                background=[("selected", ACCENT)],
                                         foreground=[("selected", WHITE)])


# ──────────────────────────────────────────────────────────────────
# ABA CLIENTES
# ──────────────────────────────────────────────────────────────────

class AbaClientes(ttk.Frame):
    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=(16, 12))
        self._selected_id: int | None = None
        self._build()
        self._load()

    # ── Layout ──────────────────────────────────────
    def _build(self) -> None:
        # Formulário
        form = ttk.Frame(self)
        form.pack(fill="x", pady=(0, 8))

        ttk.Label(form, text="ID").grid(row=0, column=0, sticky="e", padx=8, pady=4)
        self._entry_id = ttk.Entry(form, width=8, state="readonly")
        self._entry_id.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(form, text="Nome").grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self._entry_nome = ttk.Entry(form, width=32)
        self._entry_nome.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(form, text="E-mail").grid(row=2, column=0, sticky="e", padx=8, pady=4)
        self._entry_email = ttk.Entry(form, width=32)
        self._entry_email.grid(row=2, column=1, sticky="w", padx=8, pady=4)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 4))

        self._btn_criar     = ttk.Button(btn_frame, text="Cadastrar Cliente", style="Primary.TButton",
                                         command=self._criar)
        self._btn_atualizar = ttk.Button(btn_frame, text="Atualizar Dados",   style="Primary.TButton",
                                         command=self._atualizar, state="disabled")
        self._btn_excluir   = ttk.Button(btn_frame, text="Excluir",           style="Danger.TButton",
                                         command=self._excluir,   state="disabled")
        self._btn_limpar    = ttk.Button(btn_frame, text="Limpar Campos",     style="Secondary.TButton",
                                         command=self._limpar)

        for btn in (self._btn_criar, self._btn_atualizar, self._btn_excluir, self._btn_limpar):
            btn.pack(side="left", padx=4)

        # Status
        self._lbl_status = ttk.Label(self, text="", style="Status.TLabel")
        self._lbl_status.pack(fill="x", pady=(0, 4))

        # Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(
            tree_frame, columns=["ID", "Nome", "E-mail"],
            show="headings", selectmode="browse",
        )
        for col, w in [("ID", 60), ("Nome", 200), ("E-mail", 260)]:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        ttk.Button(self, text="Atualizar Lista", style="Secondary.TButton",
                   command=self._load).pack(anchor="w", pady=(4, 0))

    # ── Dados ────────────────────────────────────────
    def _load(self) -> None:
        self._tree.delete(*self._tree.get_children())
        for c in repo_cli.listar_clientes():
            self._tree.insert("", "end", values=(c["id"], c["nome"], c["email"]))

    def _on_select(self, _event=None) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0], "values")
        self._selected_id = int(values[0])
        _set_entry(self._entry_id,    str(values[0]))
        _set_entry(self._entry_nome,  values[1])
        _set_entry(self._entry_email, values[2])
        self._btn_atualizar.config(state="normal")
        self._btn_excluir.config(state="normal")

    def _criar(self) -> None:
        dados = self._validar_campos()
        if dados is None:
            return
        nome, email = dados
        try:
            repo_cli.criar_cliente(nome, email)
            self._set_status("✓ Cliente cadastrado com sucesso.", ok=True)
            self._limpar()
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _atualizar(self) -> None:
        if self._selected_id is None:
            return
        dados = self._validar_campos()
        if dados is None:
            return
        nome, email = dados
        try:
            repo_cli.atualizar_cliente(self._selected_id, nome, email)
            self._set_status("✓ Dados atualizados.", ok=True)
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _excluir(self) -> None:
        if self._selected_id is None:
            return
        if messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este registro? Esta ação não pode ser desfeita.",
        ):
            try:
                repo_cli.excluir_cliente(self._selected_id)
                self._set_status("✓ Registro removido.", ok=True)
                self._limpar()
                self._load()
            except Exception as exc:
                self._set_status(f"✗ Erro: {exc}", ok=False)

    def _limpar(self) -> None:
        self._selected_id = None
        _set_entry(self._entry_id,    "")
        _set_entry(self._entry_nome,  "")
        _set_entry(self._entry_email, "")
        self._btn_atualizar.config(state="disabled")
        self._btn_excluir.config(state="disabled")
        for item in self._tree.selection():
            self._tree.selection_remove(item)

    def _validar_campos(self) -> tuple[str, str] | None:
        nome = self._entry_nome.get().strip()
        email = self._entry_email.get().strip()
        if not nome:
            self._set_status("⚠ Informe o nome do cliente.", ok=False)
            return None
        if not email:
            self._set_status("⚠ Informe o e-mail do cliente.", ok=False)
            return None
        return nome, email

    def _set_status(self, msg: str, *, ok: bool) -> None:
        style = "Status.TLabel" if ok else "StatusErr.TLabel"
        self._lbl_status.configure(text=msg, style=style)


# ──────────────────────────────────────────────────────────────────
# ABA DESTINOS
# ──────────────────────────────────────────────────────────────────

class AbaDestinos(ttk.Frame):
    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=(16, 12))
        self._selected_id: int | None = None
        self._build()
        self._load()

    def _build(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill="x", pady=(0, 8))

        fields = [("ID", 8, True), ("Nome", 32, False), ("País", 24, False), ("Preço", 12, False)]
        self._entries: dict[str, ttk.Entry] = {}
        for row, (label, width, readonly) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="e", padx=8, pady=4)
            state = "readonly" if readonly else "normal"
            e = ttk.Entry(form, width=width, state=state)
            e.grid(row=row, column=1, sticky="w", padx=8, pady=4)
            self._entries[label] = e

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 4))

        self._btn_criar     = ttk.Button(btn_frame, text="Cadastrar Destino", style="Primary.TButton",
                                         command=self._criar)
        self._btn_atualizar = ttk.Button(btn_frame, text="Atualizar Dados",   style="Primary.TButton",
                                         command=self._atualizar, state="disabled")
        self._btn_excluir   = ttk.Button(btn_frame, text="Excluir",           style="Danger.TButton",
                                         command=self._excluir,   state="disabled")
        self._btn_limpar    = ttk.Button(btn_frame, text="Limpar Campos",     style="Secondary.TButton",
                                         command=self._limpar)
        for btn in (self._btn_criar, self._btn_atualizar, self._btn_excluir, self._btn_limpar):
            btn.pack(side="left", padx=4)

        self._lbl_status = ttk.Label(self, text="", style="Status.TLabel")
        self._lbl_status.pack(fill="x", pady=(0, 4))

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(
            tree_frame, columns=["ID", "Nome", "País", "Preço (R$)"],
            show="headings", selectmode="browse",
        )
        for col, w in [("ID", 60), ("Nome", 160), ("País", 120), ("Preço (R$)", 120)]:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        ttk.Button(self, text="Atualizar Lista", style="Secondary.TButton",
                   command=self._load).pack(anchor="w", pady=(4, 0))

    def _load(self) -> None:
        self._tree.delete(*self._tree.get_children())
        for d in repo_dst.listar_destinos():
            self._tree.insert("", "end", values=(d["id"], d["nome"], d["pais"], f"{d['preco']:.2f}"))

    def _on_select(self, _event=None) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0], "values")
        self._selected_id = int(values[0])
        for key, val in zip(["ID", "Nome", "País", "Preço"], values):
            _set_entry(self._entries[key], str(val))
        self._btn_atualizar.config(state="normal")
        self._btn_excluir.config(state="normal")

    def _criar(self) -> None:
        dados = self._validar_campos()
        if dados is None:
            return
        nome, pais, preco = dados
        try:
            repo_dst.criar_destino(nome, pais, preco)
            self._set_status("✓ Destino cadastrado com sucesso.", ok=True)
            self._limpar()
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _atualizar(self) -> None:
        if self._selected_id is None:
            return
        dados = self._validar_campos()
        if dados is None:
            return
        nome, pais, preco = dados
        try:
            repo_dst.atualizar_destino(self._selected_id, nome, pais, preco)
            self._set_status("✓ Dados atualizados.", ok=True)
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _excluir(self) -> None:
        if self._selected_id is None:
            return
        if messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este registro? Esta ação não pode ser desfeita.",
        ):
            try:
                repo_dst.excluir_destino(self._selected_id)
                self._set_status("✓ Registro removido.", ok=True)
                self._limpar()
                self._load()
            except Exception as exc:
                self._set_status(f"✗ Erro: {exc}", ok=False)

    def _limpar(self) -> None:
        self._selected_id = None
        for e in self._entries.values():
            _set_entry(e, "")
        self._btn_atualizar.config(state="disabled")
        self._btn_excluir.config(state="disabled")
        for item in self._tree.selection():
            self._tree.selection_remove(item)

    def _validar_campos(self) -> tuple[str, str, float] | None:
        nome = self._entries["Nome"].get().strip()
        pais = self._entries["País"].get().strip()
        preco_texto = self._entries["Preço"].get().strip().replace(",", ".")
        if not nome:
            self._set_status("⚠ Informe o nome do destino.", ok=False)
            return None
        if not pais:
            self._set_status("⚠ Informe o país do destino.", ok=False)
            return None
        if not preco_texto:
            self._set_status("⚠ Informe o preço do pacote.", ok=False)
            return None
        try:
            preco = float(preco_texto)
        except ValueError:
            self._set_status("⚠ Informe um preço numérico válido.", ok=False)
            return None
        if preco < 0:
            self._set_status("⚠ O preço não pode ser negativo.", ok=False)
            return None
        return nome, pais, preco

    def _set_status(self, msg: str, *, ok: bool) -> None:
        style = "Status.TLabel" if ok else "StatusErr.TLabel"
        self._lbl_status.configure(text=msg, style=style)


# ──────────────────────────────────────────────────────────────────
# ABA VENDAS
# ──────────────────────────────────────────────────────────────────

class AbaVendas(ttk.Frame):
    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=(16, 12))
        self._selected_id: int | None = None
        self._clientes: list[dict] = []
        self._destinos: list[dict] = []
        self._build()
        self._load_combos()
        self._load()

    def _build(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill="x", pady=(0, 8))

        # ID
        ttk.Label(form, text="ID").grid(row=0, column=0, sticky="e", padx=8, pady=4)
        self._entry_id = ttk.Entry(form, width=8, state="readonly")
        self._entry_id.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        # Cliente (Combobox)
        ttk.Label(form, text="Cliente").grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self._cb_cliente = ttk.Combobox(form, width=32, state="readonly")
        self._cb_cliente.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        # Destino (Combobox)
        ttk.Label(form, text="Destino").grid(row=2, column=0, sticky="e", padx=8, pady=4)
        self._cb_destino = ttk.Combobox(form, width=32, state="readonly")
        self._cb_destino.grid(row=2, column=1, sticky="w", padx=8, pady=4)

        # Data
        ttk.Label(form, text="Data Viagem").grid(row=3, column=0, sticky="e", padx=8, pady=4)
        self._entry_data = ttk.Entry(form, width=14)
        self._entry_data.grid(row=3, column=1, sticky="w", padx=8, pady=4)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 4))

        self._btn_criar     = ttk.Button(btn_frame, text="Registrar Venda",  style="Primary.TButton",
                                         command=self._criar)
        self._btn_atualizar = ttk.Button(btn_frame, text="Atualizar Dados",  style="Secondary.TButton",
                                         command=self._atualizar, state="disabled")
        self._btn_excluir   = ttk.Button(btn_frame, text="Excluir",          style="Danger.TButton",
                                         command=self._excluir,   state="disabled")
        self._btn_limpar    = ttk.Button(btn_frame, text="Limpar Campos",    style="Secondary.TButton",
                                         command=self._limpar)
        for btn in (self._btn_criar, self._btn_atualizar, self._btn_excluir, self._btn_limpar):
            btn.pack(side="left", padx=4)

        self._lbl_status = ttk.Label(self, text="", style="Status.TLabel")
        self._lbl_status.pack(fill="x", pady=(0, 4))

        # Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(
            tree_frame, columns=["ID", "Cliente", "Destino", "Data"],
            show="headings", selectmode="browse",
        )
        for col, w in [("ID", 60), ("Cliente", 180), ("Destino", 180), ("Data", 120)]:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        ttk.Button(self, text="Atualizar Lista", style="Secondary.TButton",
                   command=self._load).pack(anchor="w", pady=(4, 0))

    def _load_combos(self) -> None:
        self._clientes = repo_cli.listar_clientes()
        self._destinos = repo_dst.listar_destinos()
        self._cb_cliente["values"] = [f"{c['id']} – {c['nome']}" for c in self._clientes]
        self._cb_destino["values"] = [f"{d['id']} – {d['nome']} ({d['pais']})" for d in self._destinos]

    def _load(self) -> None:
        self._tree.delete(*self._tree.get_children())
        for v in repo_ven.listar_vendas():
            self._tree.insert("", "end",
                              values=(v["id"], v["nome_cliente"], v["nome_destino"], v["data_viagem"]),
                              tags=(str(v.get("cliente_id", "")), str(v.get("destino_id", ""))))

    def _on_select(self, _event=None) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        item = self._tree.item(sel[0])
        values = item["values"]
        tags   = item["tags"]

        self._selected_id = int(values[0])
        _set_entry(self._entry_id,   str(values[0]))
        _set_entry(self._entry_data, str(values[3]))

        # Reselecionar comboboxes pelo ID armazenado na tag
        cli_id = int(tags[0]) if tags else None
        dst_id = int(tags[1]) if len(tags) > 1 else None
        for i, c in enumerate(self._clientes):
            if c["id"] == cli_id:
                self._cb_cliente.current(i)
                break
        for i, d in enumerate(self._destinos):
            if d["id"] == dst_id:
                self._cb_destino.current(i)
                break

        self._btn_atualizar.config(state="normal")
        self._btn_excluir.config(state="normal")

    def _extract_id(self, combobox: ttk.Combobox) -> int:
        return int(combobox.get().split(" – ")[0])

    def _criar(self) -> None:
        dados = self._validar_campos()
        if dados is None:
            return
        cli_id, dst_id, data = dados
        try:
            repo_ven.criar_venda(cli_id, dst_id, data)
            self._set_status("✓ Venda cadastrada com sucesso.", ok=True)
            self._limpar()
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _atualizar(self) -> None:
        if self._selected_id is None:
            return
        dados = self._validar_campos()
        if dados is None:
            return
        cli_id, dst_id, data = dados
        try:
            repo_ven.atualizar_venda(self._selected_id, cli_id, dst_id, data)
            self._set_status("✓ Dados atualizados.", ok=True)
            self._load()
        except Exception as exc:
            self._set_status(f"✗ Erro: {exc}", ok=False)

    def _excluir(self) -> None:
        if self._selected_id is None:
            return
        if messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este registro? Esta ação não pode ser desfeita.",
        ):
            try:
                repo_ven.excluir_venda(self._selected_id)
                self._set_status("✓ Registro removido.", ok=True)
                self._limpar()
                self._load()
            except Exception as exc:
                self._set_status(f"✗ Erro: {exc}", ok=False)

    def _limpar(self) -> None:
        self._selected_id = None
        _set_entry(self._entry_id,   "")
        _set_entry(self._entry_data, "")
        self._cb_cliente.set("")
        self._cb_destino.set("")
        self._btn_atualizar.config(state="disabled")
        self._btn_excluir.config(state="disabled")
        for item in self._tree.selection():
            self._tree.selection_remove(item)

    def _validar_campos(self) -> tuple[int, int, str] | None:
        cliente = self._cb_cliente.get().strip()
        destino = self._cb_destino.get().strip()
        data = self._entry_data.get().strip()
        if not cliente:
            self._set_status("⚠ Selecione um cliente.", ok=False)
            return None
        if not destino:
            self._set_status("⚠ Selecione um destino.", ok=False)
            return None
        if not data:
            self._set_status("⚠ Informe a data da viagem.", ok=False)
            return None
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            self._set_status("⚠ Use a data no formato AAAA-MM-DD.", ok=False)
            return None
        return self._extract_id(self._cb_cliente), self._extract_id(self._cb_destino), data

    def _set_status(self, msg: str, *, ok: bool) -> None:
        style = "Status.TLabel" if ok else "StatusErr.TLabel"
        self._lbl_status.configure(text=msg, style=style)


# ──────────────────────────────────────────────────────────────────
# Utilitário
# ──────────────────────────────────────────────────────────────────

def _set_entry(entry: ttk.Entry, value: str) -> None:
    """Define o valor de um Entry independentemente do seu estado."""
    state = str(entry.cget("state"))
    entry.config(state="normal")
    entry.delete(0, "end")
    entry.insert(0, value)
    entry.config(state=state)


# ──────────────────────────────────────────────────────────────────
# Ponto de entrada
# ──────────────────────────────────────────────────────────────────

def main() -> None:
    root = tk.Tk()
    root.title("Agência de Viagens — Painel Administrativo")
    root.geometry("1040x700")
    root.configure(bg=BG)

    _apply_style(root)

    # Cabeçalho com a mesma hierarquia da aplicação web.
    header = tk.Frame(root, bg=BG, padx=20, pady=16)
    header.pack(fill="x")
    tk.Label(
        header, text="✈ Agência de Viagens",
        bg=BG, fg=TEXT, font=("Inter", 22, "bold"), anchor="w",
    ).pack(fill="x")
    tk.Label(
        header, text="Portal Administrativo · DB Relacional",
        bg=BG, fg=TEXT, font=("Inter", 12, "italic"), anchor="w", pady=7,
    ).pack(fill="x")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    notebook.add(AbaClientes(notebook), text="  👤 Clientes  ")
    notebook.add(AbaDestinos(notebook), text="  📍 Destinos  ")
    notebook.add(AbaVendas(notebook),   text="  🎫 Vendas  ")

    root.mainloop()


if __name__ == "__main__":
    main()
