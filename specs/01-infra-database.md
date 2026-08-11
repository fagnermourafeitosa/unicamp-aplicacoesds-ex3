# Spec 01 — Infraestrutura & Conexões de Banco de Dados

## Problem Statement

O sistema de agência de viagens necessita conectar-se simultaneamente a dois bancos de dados em nuvem: Supabase (PostgreSQL) para dados transacionais/relacionais e MongoDB Atlas para dados documentais (comentários). Sem essa camada de infraestrutura configurada corretamente, nenhuma das interfaces — Gradio ou Tkinter — pode funcionar.

## Solution

Criar um módulo de configuração de ambiente e um módulo de conexão (database layer) que instancia e exporta os dois clientes de banco de dados a partir de variáveis de ambiente, garantindo que todas as partes da aplicação usem a mesma instância de conexão.

## User Stories

1. Como desenvolvedor, quero ler as credenciais do Supabase a partir de variáveis de ambiente, para que eu não exponha dados sensíveis no código-fonte.
2. Como desenvolvedor, quero ler as credenciais do MongoDB Atlas a partir de variáveis de ambiente, para que a conexão seja configurável sem alterar o código.
3. Como desenvolvedor, quero uma função `get_supabase_client()` que retorne uma instância autenticada do cliente Supabase, para que os módulos de repositório possam usá-la sem se preocupar com inicialização.
4. Como desenvolvedor, quero uma função `get_mongo_collection(name)` que retorne uma coleção MongoDB pronta para uso, para que os módulos de repositório possam usá-la diretamente.
5. Como desenvolvedor, quero que a aplicação falhe com uma mensagem de erro clara caso alguma variável de ambiente obrigatória não esteja definida, para que erros de configuração sejam diagnosticados rapidamente.
6. Como DBA/administrador, quero que o schema PostgreSQL (tabelas `clientes`, `destinos`, `vendas`) seja documentado com os tipos exatos de cada coluna, para que possa ser recriado em outro ambiente se necessário.
7. Como desenvolvedor, quero um script ou instrução que crie as tabelas no Supabase (via SQL), para que o ambiente possa ser reproduzido do zero.

## Implementation Decisions

- O módulo `config.py` carregará as variáveis de ambiente via `python-dotenv` a partir do arquivo `.env` na raiz do projeto.
- As variáveis obrigatórias são: `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `MONGODB_URI` (ou `MONGODB_CONN`).
- O módulo `database.py` exportará dois helpers: `get_supabase_client()` (usando o SDK `supabase-py`) e `get_mongo_db()` (usando `pymongo`).
- As conexões devem ser singleton por processo (instanciadas uma vez e reutilizadas), usando o padrão de módulo Python (variável de módulo).
- Schema Supabase (PostgreSQL):

  ```
  clientes  (id SERIAL PK, nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL)
  destinos  (id SERIAL PK, nome TEXT NOT NULL, pais TEXT NOT NULL, preco NUMERIC NOT NULL)
  vendas    (id SERIAL PK, cliente_id INT FK clientes.id, destino_id INT FK destinos.id, data_viagem DATE NOT NULL)
  ```

- Coleção MongoDB (`comentarios`): documento com campos `cliente_id` (int), `destino_id` (int), `texto` (string), `data` (datetime).
- O banco MongoDB a ser usado será chamado `agencia_viagens`.
- As dependências (`supabase`, `pymongo`, `python-dotenv`) devem ser registradas no `pyproject.toml`.

## Testing Decisions

- Um bom teste verifica apenas comportamento externo: se os clientes são retornados sem erro quando as variáveis estão presentes, e se um `ValueError` (ou similar) é lançado quando estão ausentes.
- Módulo a testar: `database.py` — especificamente a função que valida variáveis de ambiente.
- Usar `monkeypatch` do pytest para injetar/remover variáveis de ambiente nos testes, sem depender do arquivo `.env` real.
- Não testar a conexão real com os bancos em testes unitários — apenas a lógica de configuração.

## Tasks

- [ ] Adicionar dependências `supabase`, `pymongo[srv]` e `python-dotenv` ao `pyproject.toml`
- [ ] Criar `src/ds_unicamp_applicada_3/config.py` para carregamento de variáveis de ambiente
- [ ] Criar `src/ds_unicamp_applicada_3/database.py` com `get_supabase_client()` e `get_mongo_db()`
- [ ] Documentar o SQL de criação das tabelas no Supabase (em `specs/` ou `README.md`)
- [ ] Verificar que `uv run` carrega o `.env` corretamente no ambiente de dev

## Out of Scope

- Migrations automáticas de banco de dados (Alembic, etc.) — o schema é gerenciado manualmente no Supabase Dashboard.
- Pool avançado de conexões ou reconexão automática em caso de falha.
- Autenticação de usuários (row-level security no Supabase).

## Further Notes

- O arquivo `.env.example` já contém o template das variáveis necessárias — manter sincronizado com `config.py`.
- O `SUPABASE_PUBLISHABLE_KEY` é a anon/public key — adequada para uso no lado do servidor com Python.
