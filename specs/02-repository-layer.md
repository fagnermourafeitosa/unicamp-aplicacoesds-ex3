# Spec 02 — Camada de Repositório (Persistência Compartilhada)

## Problem Statement

Tanto a interface Gradio quanto a interface Tkinter precisam realizar operações de leitura e escrita nos bancos de dados. Sem uma camada de repositório centralizada, a lógica de acesso a dados ficaria duplicada em cada interface, dificultando manutenção e testes.

## Solution

Criar módulos de repositório independentes de interface — um para cada entidade do domínio — que encapsulam toda a lógica de acesso a dados (Supabase e MongoDB). As interfaces Gradio e Tkinter consumirão esses repositórios diretamente, sem conhecer os detalhes dos SDKs.

## User Stories

1. Como desenvolvedor, quero uma função `criar_cliente(nome, email)` que insira um novo cliente no Supabase e retorne o registro criado, para que as interfaces não precisem conhecer o SDK.
2. Como desenvolvedor, quero uma função `listar_clientes()` que retorne todos os clientes cadastrados no Supabase, para exibição nas interfaces.
3. Como desenvolvedor, quero uma função `atualizar_cliente(id, nome, email)` que atualize os dados de um cliente existente no Supabase, para suportar o CRUD da interface Tkinter.
4. Como desenvolvedor, quero uma função `excluir_cliente(id)` que remova um cliente do Supabase, para suportar o CRUD da interface Tkinter.
5. Como desenvolvedor, quero funções análogas (`criar_destino`, `listar_destinos`, `atualizar_destino`, `excluir_destino`) para a entidade `destinos`, para garantir cobertura completa de CRUD.
6. Como desenvolvedor, quero funções análogas (`criar_venda`, `listar_vendas`, `atualizar_venda`, `excluir_venda`) para a entidade `vendas`, incluindo resolução dos nomes de cliente e destino na listagem.
7. Como desenvolvedor, quero uma função `criar_comentario(cliente_id, destino_id, texto)` que insira um documento na coleção `comentarios` do MongoDB com a data atual, para salvar avaliações dos clientes.
8. Como desenvolvedor, quero uma função `listar_comentarios()` que retorne todos os documentos da coleção `comentarios`, para exibição na interface Gradio.

## Implementation Decisions

- Estrutura de módulos dentro de `src/ds_unicamp_applicada_3/`:
  - `repositories/clientes.py` — CRUD completo sobre a tabela `clientes` no Supabase
  - `repositories/destinos.py` — CRUD completo sobre a tabela `destinos` no Supabase
  - `repositories/vendas.py` — CRUD completo sobre a tabela `vendas` no Supabase
  - `repositories/comentarios.py` — Create + Read sobre a coleção `comentarios` no MongoDB
- Cada função de repositório chama `get_supabase_client()` ou `get_mongo_db()` (da Spec 01) internamente; não recebe conexão como parâmetro.
- As funções de listagem retornam listas de dicionários Python simples (não objetos ORM), para máxima compatibilidade com as duas interfaces.
- A função `listar_vendas()` deve fazer join lógico (via chamadas adicionais ao Supabase ou usando PostgREST `select` com expansão de FK) para retornar nome do cliente e nome do destino junto com os dados da venda.
- Erros de banco (conexão, constraint violation) devem ser deixados propagar como exceções nativas — o tratamento é responsabilidade das interfaces.

## Testing Decisions

- Um bom teste verifica apenas a saída das funções de repositório dado um estado de banco conhecido, não como a query foi montada internamente.
- Os testes de repositório devem usar o banco real (integração) ou um mock do cliente Supabase/PyMongo — preferir mock para testes unitários rápidos.
- Usar `unittest.mock.MagicMock` para substituir as respostas dos SDKs e verificar que as funções retornam os dados formatados corretamente.
- Módulos a testar: todos os quatro módulos de repositório.

## Tasks

- [ ] Criar diretório `src/ds_unicamp_applicada_3/repositories/`
- [ ] Criar `repositories/__init__.py`
- [ ] Implementar `repositories/clientes.py` com `criar_cliente`, `listar_clientes`, `atualizar_cliente`, `excluir_cliente`
- [ ] Implementar `repositories/destinos.py` com `criar_destino`, `listar_destinos`, `atualizar_destino`, `excluir_destino`
- [ ] Implementar `repositories/vendas.py` com `criar_venda`, `listar_vendas`, `atualizar_venda`, `excluir_venda`
- [ ] Implementar `repositories/comentarios.py` com `criar_comentario` e `listar_comentarios`
- [ ] Verificar manualmente cada função contra o Supabase e MongoDB reais

## Out of Scope

- Paginação ou filtros avançados nas listagens.
- Validação de dados de entrada (e.g., email válido) — responsabilidade das interfaces.
- Soft delete (exclusão lógica) — o `excluir_*` remove o registro definitivamente.

## Further Notes

- Esta spec depende inteiramente da Spec 01 (infraestrutura) estar concluída.
- A interface da camada de repositório deve ser estável: mudanças nos nomes das funções quebrarão as duas interfaces (Gradio e Tkinter) simultaneamente.
