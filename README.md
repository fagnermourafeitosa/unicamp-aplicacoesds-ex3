# Agência de Viagens: Cadastro e Comentários

Este repositório contém a implementação da "Tarefa Aula 3 — Agência de Viagens". O projeto propõe o desenvolvimento de um sistema com foco na integração simultânea de dois tipos diferentes de bancos de dados (persistência poliglota).

O sistema é composto por duas interfaces que operam sobre a mesma base de dados:
1. **Aplicação Web (Gradio)**: Focada no usuário para operações de cadastro e avaliações.
2. **Aplicação Desktop (Tkinter)**: Focada na administração completa dos dados (CRUD).

## 🗄️ Estrutura de Banco de Dados (Persistência Poliglota)

O diferencial deste projeto é o uso combinado de dois bancos de dados em nuvem, aproveitando o melhor de cada modelagem:

### 1. Supabase (PostgreSQL) - Banco Relacional
Usado para dados estruturados, transacionais e formalizados.
- `clientes`: `id`, `nome`, `email`
- `destinos`: `id`, `nome`, `país`, `preço`
- `vendas`: `id`, `cliente_id`, `destino_id`, `data_viagem` *(Tabela associativa relacionando clientes e destinos)*

### 2. MongoDB Atlas - Banco Não-Relacional (NoSQL)
Usado para dados menos rígidos e textuais, utilizando formato de documentos.
- `comentarios`: `cliente_id`, `destino_id`, `texto`, `data`

---

## 💻 Interfaces

### Parte 1 — Aplicação Web (Gradio)
Permite o cadastro de informações de vendas e as avaliações pós-viagem:
- **Cadastros Básicos**: Criação de clientes, destinos e vendas (gravação no Supabase).
- **Avaliações**: Input de texto livre para clientes comentarem sobre viagens específicas (gravação no MongoDB Atlas).
- **Consulta**: Visualização em lista/tabela de todos os comentários deixados pelos clientes.

### Parte 2 — Aplicação Desktop de Administração (Tkinter)
Interface CRUD voltada para administração completa e gerenciamento do sistema operando sobre o Supabase:
- **Cadastrar (Create)**: Inserir novos clientes, destinos e vendas.
- **Consultar (Read)**: Visualização visual de dados existentes via `ttk.Treeview`.
- **Atualizar (Update)**: Carregamento de dados para edição e atualização na base.
- **Excluir (Delete)**: Remoção de registros do banco, com aviso de confirmação.

---

## 📁 Estrutura do Projeto

```
ds-unicamp-applicada-3/
├── .claude/
│   └── napkin.md                 # Runbook de orientações recorrentes do projeto
├── .env                          # Credenciais locais (não commitado)
├── .env.example                  # Template de variáveis de ambiente
├── pyproject.toml                # Dependências e metadados do projeto (uv)
├── AGENTS.md                     # Regras de comportamento para agentes de IA
│
├── specs/                        # Especificações técnicas
│   ├── exercise.md               # Enunciado original do exercício
│   ├── 01-infra-database.md      # Spec: infraestrutura e conexões de banco
│   ├── 02-repository-layer.md    # Spec: camada de repositório (CRUD)
│   ├── 03-gradio-web-app.md      # Spec: aplicação web Gradio
│   ├── 04-tkinter-admin-app.md   # Spec: interface desktop Tkinter
│   └── schema.sql                # DDL para criação das tabelas no Supabase
│
├── scripts/
│   ├── up-supabase.sh            # Cria as tabelas no Supabase
│   ├── run-gradio.sh             # Inicia a aplicação web
│   └── run-tkinter.sh            # Inicia o painel desktop
│
└── src/ds_unicamp_applicada_3/
    ├── __init__.py
    ├── config.py                 # Carregamento de variáveis de ambiente
    ├── database.py               # Singletons de conexão Supabase + MongoDB
    ├── app_gradio.py             # Aplicação web (Gradio)
    ├── app_tkinter.py            # Aplicação desktop (Tkinter)
    └── repositories/
        ├── __init__.py
        ├── clientes.py           # CRUD clientes → Supabase
        ├── destinos.py           # CRUD destinos → Supabase
        ├── vendas.py             # CRUD vendas → Supabase (com resolução de nomes FK)
        └── comentarios.py        # Create + Read comentários → MongoDB
```

---

## 🛠️ Tecnologias Utilizadas
- **Python** gerenciado através do [**uv**](https://github.com/astral-sh/uv).
- **Gradio** (Interface Web)
- **Tkinter** (Interface Desktop nativa)
- **Supabase / PostgreSQL** (Banco Relacional)
- **MongoDB Atlas** (Banco NoSQL Documental)

---

## 🚀 Como Executar

### 1. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

### 2. Instale as dependências

```bash
~/.local/bin/uv sync
```

### 3. Crie as tabelas no Supabase

Execute o script abaixo (requer `psql` instalado e as variáveis de ambiente configuradas no `.env`):

```bash
bash scripts/up-supabase.sh
```

Ou execute manualmente o SQL em `specs/schema.sql` pelo **Supabase Dashboard → SQL Editor**.

### 4. Execute a aplicação desejada

**Aplicação Web (Gradio):**
```bash
bash scripts/run-gradio.sh
```
Acesse em `http://localhost:7860`.

**Aplicação Desktop (Tkinter):**
```bash
bash scripts/run-tkinter.sh
```
