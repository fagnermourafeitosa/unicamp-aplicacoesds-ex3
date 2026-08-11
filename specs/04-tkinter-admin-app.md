# Spec 04 — Interface Desktop de Administração (Tkinter CRUD)

## Problem Statement

O administrador da agência de viagens precisa de uma interface desktop para gerenciar completamente os dados cadastrados — incluindo editar e excluir registros — operações não disponíveis na interface web Gradio. Sem essa ferramenta, alterações incorretas nos dados exigiriam acesso direto ao banco de dados.

## Solution

Construir uma aplicação desktop com Tkinter que conecta ao mesmo Supabase da aplicação Gradio e oferece as quatro operações CRUD (Create, Read, Update, Delete) para as entidades `clientes`, `destinos` e `vendas`. A interface utilizará abas (Notebook) para separar o gerenciamento de cada entidade, com uma Treeview para listagem e formulários para edição.

## User Stories

1. Como administrador, quero ver uma janela com três abas ("Clientes", "Destinos", "Vendas") ao abrir a aplicação, para ter acesso organizado a cada entidade.
2. Como administrador, quero que ao selecionar uma aba, a lista de registros existentes seja carregada automaticamente em uma tabela visual (Treeview), para ter visibilidade imediata dos dados.
3. Como administrador, quero preencher um formulário (campos Entry) na aba "Clientes" e clicar em "Cadastrar", para inserir novos clientes no Supabase.
4. Como administrador, quero clicar em um registro na Treeview de Clientes e ver seus dados carregados automaticamente nos campos de formulário, para poder editá-los.
5. Como administrador, quero editar os campos carregados e clicar em "Atualizar", para salvar as alterações do cliente no banco.
6. Como administrador, quero selecionar um registro na Treeview e clicar em "Excluir", para remover o cliente do banco após confirmar em um diálogo de confirmação.
7. Como administrador, quero clicar em "Atualizar Lista" para recarregar a Treeview com os dados mais recentes do banco, para ver efeitos de operações recentes.
8. Como administrador, quero funcionalidades análogas (Create, Read, Update, Delete) na aba "Destinos" para gerenciar destinos de viagem.
9. Como administrador, quero funcionalidades análogas (Create, Read, Update, Delete) na aba "Vendas" para gerenciar registros de vendas, com dropdowns para selecionar cliente e destino.
10. Como administrador, quero receber mensagens de sucesso ou erro em um label/messagebox após cada operação, para confirmar que a ação foi realizada.
11. Como administrador, quero que a exclusão de um registro exiba um diálogo de confirmação (`messagebox.askyesno`) antes de efetivar a remoção, para evitar deleções acidentais.

## Implementation Decisions

- O ponto de entrada da aplicação Tkinter será `src/ds_unicamp_applicada_3/app_tkinter.py`.
- A estrutura da janela usará `ttk.Notebook` como container principal com três `ttk.Frame` filhos (um por entidade).
- Cada aba seguirá o mesmo layout padrão:
  - Área superior: formulário com `ttk.Label` + `ttk.Entry` para cada campo da entidade.
  - Botões de ação: "Cadastrar", "Atualizar", "Excluir", "Limpar Campos" e "Atualizar Lista".
  - Área inferior: `ttk.Treeview` com colunas correspondentes às colunas da tabela, com scrollbar vertical.
- A seleção de um item na Treeview (`<<TreeviewSelect>>`) dispara um evento que popula os campos do formulário automaticamente.
- As abas de Vendas usarão `ttk.Combobox` (em vez de `ttk.Entry` puro) para os campos `cliente_id` e `destino_id`, exibindo nomes e carregando IDs internamente.
- As funções de callback chamarão diretamente os repositórios da Spec 02 (sem lógica de negócio própria).
- O estado do registro selecionado (ID) será mantido em uma variável de instância da classe ou em uma variável de closure do frame.
- A aplicação será iniciada com `root.mainloop()`.
- Tkinter é biblioteca padrão do Python — nenhuma dependência adicional necessária.

## Testing Decisions

- Testes automatizados de UI Tkinter são incomuns e de alto custo; o foco estará nos repositórios (Spec 02).
- Verificação manual: rodar a aplicação e executar cada operação CRUD em cada aba, verificando no Supabase Dashboard que os dados foram alterados.
- Verificar especificamente: (a) carregamento de dados na Treeview ao abrir cada aba; (b) preenchimento do formulário ao clicar em um item; (c) diálogo de confirmação ao excluir; (d) atualização da Treeview após cada operação.

## Tasks

- [ ] Criar `src/ds_unicamp_applicada_3/app_tkinter.py` com janela principal e `ttk.Notebook`
- [ ] Implementar aba "Clientes" com formulário (nome, email), Treeview e botões CRUD completos
- [ ] Implementar aba "Destinos" com formulário (nome, país, preço), Treeview e botões CRUD completos
- [ ] Implementar aba "Vendas" com Combobox de cliente/destino, campo de data, Treeview e botões CRUD completos
- [ ] Implementar lógica de `<<TreeviewSelect>>` para popular formulário ao clicar em item
- [ ] Implementar diálogo de confirmação antes de excluir (`messagebox.askyesno`)
- [ ] Testar cada operação CRUD manualmente em cada aba
- [ ] Registrar o comando de execução no `README.md` (ex: `uv run python src/.../app_tkinter.py`)

## Out of Scope

- Gerenciamento de comentários MongoDB via interface Tkinter (somente leitura/escrita no Supabase).
- Autenticação/login de administrador.
- Exportação de dados (CSV, Excel, etc.).
- Temas visuais avançados além do padrão `ttk`.

## Further Notes

- Esta spec depende da Spec 02 (repositórios) estar concluída.
- O Tkinter corre no processo principal com seu próprio event loop (`mainloop`); não pode ser executado simultaneamente com o Gradio no mesmo processo — são aplicações separadas.
- A aba de Vendas é a mais complexa: requer buscar listas de clientes e destinos do Supabase para popular os Comboboxes ao carregar a aba.
