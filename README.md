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

*Nota: O layout Tkinter utilizará abas (`Notebook`) para separar a gerência das entidades.*

---

## 🛠️ Tecnologias Utilizadas
- **Python** gerenciado através do [**uv**](https://github.com/astral-sh/uv).
- **Gradio** (Interface Web)
- **Tkinter** (Interface Desktop nativa)
- **Supabase / PostgreSQL** (Banco Relacional)
- **MongoDB Atlas** (Banco NoSQL Documental)

## 🚀 Como Executar

1. Certifique-se de ativar o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```
2. Instale as dependências (a serem definidas no projeto).
3. Preencha o arquivo `.env` baseado no `.env.example` com as credenciais do Supabase e MongoDB Atlas fornecidas no repositório.
4. Rode a aplicação desejada (o comando exato de inicialização será definido).
