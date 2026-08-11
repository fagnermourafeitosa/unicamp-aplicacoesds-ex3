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
- As abas de Vendas usarão `ttk.Combobox` (em vez de `ttk.Entry` puro) para os campos `cliente_id` e `destino_id`, exibindo nomes e carregando IDs internamente. O formato exibido no Combobox será `"<id> – <nome>"` (ex: `"1 – Maria Silva"`); a extração do ID numérico na submissão do formulário é feita via `int(valor.split(' – ')[0])`. Essa convenção deve ser consistente entre todos os Comboboxes da aplicação.
- As funções de callback chamarão diretamente os repositórios da Spec 02 (sem lógica de negócio própria).
- O estado do registro selecionado (ID) será mantido em uma variável de instância da classe ou em uma variável de closure do frame.
- A aplicação será iniciada com `root.mainloop()`.
- Tkinter é biblioteca padrão do Python — nenhuma dependência adicional necessária.

## Design Visual

> Aplicado seguindo a skill `frontend-design`. Tkinter não suporta CSS — as decisões de cor e tipografia são aplicadas via `ttk.Style` e opções de widget. A paleta é compartilhada com o Gradio para coerência sistêmica entre as duas interfaces do mesmo produto.

### Paleta de Cores

| Nome | Hex | Uso no Tkinter |
|---|---|---|
| Azul Noite | `#0D1B2A` | `background` da janela principal, fundo dos `Entry` |
| Azul Oceano | `#1B4965` | Fundo dos `ttk.Frame` de aba, fundo do `ttk.Notebook` |
| Azul Céu | `#5FA8D3` | `selectbackground` da Treeview, highlight de botão hover |
| Névoa de Altitude | `#CAE9FF` | `foreground` (texto) de Labels e Treeview |
| Âmbar Cartão de Embarque | `#E9C46A` | `background` dos botões primários (Cadastrar, Atualizar) |
| Vermelho de Alerta | `#C0392B` | `background` do botão Excluir |

### Tipografia

- **Labels e botões:** `('Inter', 11)` — ou `('Segoe UI', 11)` no Windows como fallback system sans-serif.
- **Título da janela:** `('Inter', 13, 'bold')` no `Label` de cabeçalho.
- **Treeview (dados):** `('Courier New', 10)` — monoespaçado para alinhar colunas de dados.
- **Mensagens de status:** `('Inter', 11, 'italic')`.

### Configuração via ttk.Style

```
style = ttk.Style()
style.theme_use('clam')               # base mais controlável que 'default'

style.configure('TFrame',            background='#1B4965')
style.configure('TNotebook',         background='#0D1B2A', borderwidth=0)
style.configure('TNotebook.Tab',     background='#0D1B2A', foreground='#CAE9FF',
                                     padding=[12, 6], font=('Inter', 11))
style.map('TNotebook.Tab',           background=[('selected', '#1B4965')],
                                     foreground=[('selected', '#E9C46A')])

style.configure('TLabel',            background='#1B4965', foreground='#CAE9FF',
                                     font=('Inter', 11))
style.configure('TEntry',            fieldbackground='#0D1B2A', foreground='#CAE9FF',
                                     insertcolor='#CAE9FF', borderwidth=1, relief='flat')
style.configure('TCombobox',         fieldbackground='#0D1B2A', foreground='#CAE9FF')

style.configure('Primary.TButton',   background='#E9C46A', foreground='#0D1B2A',
                                     font=('Inter', 11, 'bold'), relief='flat', padding=[8, 6])
style.map('Primary.TButton',         background=[('active', '#d4b05a')])

style.configure('Secondary.TButton', background='#1B4965', foreground='#CAE9FF',
                                     font=('Inter', 11), relief='flat', padding=[8, 6])
style.map('Secondary.TButton',       background=[('active', '#5FA8D3')])

style.configure('Danger.TButton',    background='#C0392B', foreground='#FFFFFF',
                                     font=('Inter', 11, 'bold'), relief='flat', padding=[8, 6])
style.map('Danger.TButton',          background=[('active', '#a93226')])

style.configure('Treeview',          background='#0D1B2A', foreground='#CAE9FF',
                                     fieldbackground='#0D1B2A', rowheight=28,
                                     font=('Courier New', 10))
style.configure('Treeview.Heading',  background='#1B4965', foreground='#E9C46A',
                                     font=('Inter', 11, 'bold'), relief='flat')
style.map('Treeview',                background=[('selected', '#5FA8D3')],
                                     foreground=[('selected', '#0D1B2A')])
```

### Wireframe — Janela Principal

```
┌──────────────────────────────────────────────────────────────────┐
│  ● ○ ○   Agência de Viagens — Painel Administrativo           │  ← title da janela
├──────────────────────────────────────────────────────────────────┤
│  BARRA HEADER  bg #0D1B2A, padding 12px                         │
│  Label: "Painel Administrativo"  font bold 13px #E9C46A         │
├──────────────────────────────────────────────────────────────────┤
│  ttk.Notebook                                                   │
│  [  Clientes  ]  [  Destinos  ]  [  Vendas  ]                   │
│  ↓ aba ativa: text #E9C46A, bg #1B4965                         │
│  ↓ aba inativa: text #CAE9FF opacity, bg #0D1B2A               │
├──────────────────────────────────────────────────────────────────┤
│  CONTEÚDO DA ABA (ttk.Frame bg #1B4965, padx=16 pady=12)        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  FORMULÁRIO (grid 2 colunas: labels + entries)                │  │
│  │  + BARRA DE BOTÕES (Cadastrar | Atualizar | Excluir | Limpar)│  │
│  └──────────────────────────────────────────────────────────────┘  │
│  LABEL DE STATUS  font italic 11px  |│  ← sucesso: #5FA8D3 / erro: #E9C46A  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ttk.Treeview (expand=True, fill=BOTH) + Scrollbar vertical │  │
│  │  [  Atualizar Lista  ]  botão secundário abaixo da Treeview  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Wireframe — Aba Clientes

```
FORMULÁRIO (grid, padx=8, pady=4)
──────────────────────────────────
Label ["ID"]          Entry [width=8, state=readonly]   ← preenchido ao selecionar item
Label ["Nome"]        Entry [width=32]                  ← editavel
Label ["E-mail"]      Entry [width=32]

BARRA DE BOTÕES (pack, side=LEFT, padx=4)
──────────────────────────────────
[ Cadastrar Cliente ]   style=Primary.TButton
[ Atualizar Dados ]     style=Primary.TButton  (desabilitado até selecionar item)
[ Excluir ]             style=Danger.TButton   (desabilitado até selecionar item)
[ Limpar Campos ]       style=Secondary.TButton

STATUS LABEL
──────────────────────────────────
• Vazio até a primeira ação
• Sucesso: "✓ Cliente cadastrado com sucesso."   fg=#5FA8D3
• Sucesso update: "✓ Dados atualizados."          fg=#5FA8D3
• Sucesso delete: "✓ Cliente removido."           fg=#5FA8D3
• Erro: "✗ Erro: [mensagem]"                      fg=#E9C46A

TREEVIEW  (columns=["ID", "Nome", "E-mail"], show='headings')
──────────────────────────────────
  ID   | Nome                 | E-mail
  1    | Maria Silva          | maria@email.com
  2    | João Santos          | joao@email.com

[  Atualizar Lista  ]     style=Secondary.TButton, abaixo da Treeview

SELEÇÃO DE ITEM (<<TreeviewSelect>>)
──────────────────────────────────
• Preenche os Entry com os valores do registro selecionado
• Habilita os botões "Atualizar Dados" e "Excluir"
• Deselecionar (clicar em área vazia) ou "Limpar Campos":
  volta ao estado inicial, botões desabilitados novamente
```

### Wireframe — Aba Destinos

```
FORMULÁRIO
──────────────────────────────────
Label ["ID"]     Entry [readonly]
Label ["Nome"]   Entry [width=32]     ex: "Lisboa"
Label ["País"]  Entry [width=24]     ex: "Portugal"
Label ["Preço"] Entry [width=12]     aceita float  ex: "3500.00"

BOTÕES: [ Cadastrar Destino ] [ Atualizar Dados ] [ Excluir ] [ Limpar Campos ]
Mesmo padrão de estilo e habilitação da aba Clientes.

TREEVIEW  (columns=["ID", "Nome", "País", "Preço (R$)"])
  ID | Nome     | País     | Preço (R$)
  1  | Lisboa   | Portugal  | 3.500,00
  2  | Paris    | França    | 5.200,00
```

### Wireframe — Aba Vendas

```
FORMULÁRIO
──────────────────────────────────
Label ["ID"]           Entry [readonly]
Label ["Cliente"]      Combobox [values=["1 – Maria Silva", "2 – João Santos"]]
                       Largura: 32 • Seleção extrai o ID (parte antes de ' – ')
Label ["Destino"]      Combobox [values=["1 – Lisboa (Portugal)", "2 – Paris (França)"]]
Label ["Data Viagem"]  Entry [width=14, placeholder: "AAAA-MM-DD"]

BOTÕES: [ Registrar Venda ] [ Atualizar Dados ] [ Excluir ] [ Limpar Campos ]
• "Registrar Venda" = Primary; "Excluir" = Danger; demais = Secondary
• Comboboxes são populados ao abrir a aba (chamada aos repositórios)

TREEVIEW  (columns=["ID", "Cliente", "Destino", "Data"])
  ID | Cliente      | Destino  | Data
  1  | Maria Silva  | Lisboa   | 2025-03-15
```

### Regras de copy dos componentes

| Elemento | Texto |
|---|---|
| Botão criar — Clientes | "Cadastrar Cliente" |
| Botão criar — Destinos | "Cadastrar Destino" |
| Botão criar — Vendas | "Registrar Venda" |
| Botão atualizar (todas as abas) | "Atualizar Dados" |
| Botão excluir (todas as abas) | "Excluir" |
| Botão limpar | "Limpar Campos" |
| Botão reload da Treeview | "Atualizar Lista" |
| Diálogo de confirmação | "Tem certeza que deseja excluir este registro? Esta ação não pode ser desfeita." |
| Sucesso — cadastro | "✓ [Entidade] cadastrado(a) com sucesso." |
| Sucesso — atualização | "✓ Dados atualizados." |
| Sucesso — exclusão | "✓ Registro removido." |
| Erro genérico | "✗ Erro: [mensagem técnica direta]" |

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
- Temas nativos de terceiros (ttkthemes, etc.) — o estilo visual já está definido na seção Design Visual desta spec via `ttk.Style` nativo.

## Further Notes

- Esta spec depende da Spec 02 (repositórios) estar concluída.
- O Tkinter corre no processo principal com seu próprio event loop (`mainloop`); não pode ser executado simultaneamente com o Gradio no mesmo processo — são aplicações separadas.
- A aba de Vendas é a mais complexa: requer buscar listas de clientes e destinos do Supabase para popular os Comboboxes ao carregar a aba.
