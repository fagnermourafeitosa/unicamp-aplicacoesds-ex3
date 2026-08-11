# Spec 03 — Aplicação Web (Gradio)

## Problem Statement

O usuário final da agência de viagens precisa de uma interface simples e acessível via browser para cadastrar clientes, destinos e vendas, além de escrever e visualizar comentários sobre viagens realizadas. Sem essa interface, as operações precisariam ser feitas diretamente via banco de dados, o que é inviável para usuários não técnicos.

## Solution

Construir uma aplicação web com Gradio que apresenta um formulário por entidade (clientes, destinos, vendas, comentários), cada um com seus campos correspondentes e um botão de submissão. A aplicação também exibe todos os comentários cadastrados em uma tabela consultável.

## User Stories

1. Como usuário da agência, quero preencher um formulário com nome e email e clicar em "Cadastrar Cliente", para que meus dados sejam registrados no sistema.
2. Como usuário da agência, quero preencher um formulário com nome do destino, país e preço, e clicar em "Cadastrar Destino", para que novos destinos fiquem disponíveis para venda.
3. Como usuário da agência, quero selecionar um cliente, um destino e uma data de viagem, e clicar em "Registrar Venda", para que a venda fique associada no sistema.
4. Como cliente pós-viagem, quero selecionar meu nome e o destino visitado, escrever um comentário em texto livre e clicar em "Enviar Comentário", para que minha avaliação seja salva no MongoDB.
5. Como usuário, quero clicar em "Ver Comentários" e visualizar uma tabela com todos os comentários já cadastrados (incluindo nome do cliente, destino e texto), para acompanhar as avaliações dos clientes.
6. Como usuário, quero receber uma mensagem de confirmação de sucesso (ou de erro) após cada operação de cadastro, para saber se a ação foi concluída.
7. Como usuário, quero que os dropdowns de seleção de cliente e destino (nas abas de venda e comentário) sejam preenchidos dinamicamente a partir dos dados já cadastrados no Supabase, para não precisar digitar IDs manualmente.

## Implementation Decisions

- O ponto de entrada da aplicação Gradio será `src/ds_unicamp_applicada_3/app_gradio.py`.
- A interface utilizará `gr.Blocks` com abas (`gr.Tab`) para separar as seções: "Clientes", "Destinos", "Vendas" e "Comentários".
- Cada aba conterá um `gr.Form` (ou grupo de `gr.Textbox` / `gr.Dropdown` / `gr.DatePicker`) e um `gr.Button`.
- Os dropdowns de cliente e destino serão populados no carregamento via `gr.Dropdown(choices=listar_clientes())` — sem update dinâmico em tempo real para simplificar.
- As funções de callback dos botões chamarão diretamente os repositórios da Spec 02 (sem lógica de negócio própria).
- A aba "Comentários" terá um `gr.Dataframe` ou `gr.HTML` para exibir os comentários retornados por `listar_comentarios()`.
- A aplicação será iniciada com `demo.launch()` sem autenticação.
- A dependência `gradio` deve ser registrada no `pyproject.toml`.

## Design Visual

> Aplicado seguindo a skill `frontend-design`: duas passagens (planejar → revisar → construir). As decisões abaixo são específicas ao domínio de viagens — cartões de embarque, rotas, destinos — e foram revisadas para não reproduzir defaults genéricos de IA.

### Paleta de Cores

| Nome | Hex | Uso |
|---|---|---|
| Azul Noite | `#0D1B2A` | Background base da página |
| Azul Oceano | `#1B4965` | Painéis, cards de aba |
| Azul Céu | `#5FA8D3` | Accent primário, bordas de foco |
| Névoa de Altitude | `#CAE9FF` | Texto principal sobre fundos escuros |
| Âmbar Cartão de Embarque | `#E9C46A` | CTAs, botões de ação, destaques |

### Tipografia

- **Display:** `Playfair Display` (italic) — usada com contenção nos títulos de seção; carrega a personalidade de cartaz de viagem vintage.
- **Body/UI:** `Inter` — labels, inputs, mensagens de status; legível e contemporânea.
- **Utility:** `JetBrains Mono` — IDs e dados na tabela de comentários; âncora de dados técnicos.
- Importar via Google Fonts no `theme` do Gradio ou via CSS customizado (`gr.Blocks(css=...)`.

### Tokens CSS

```css
/* Aplicar via gr.Blocks(css=CUSTOM_CSS) */
:root {
  --color-bg:        #0D1B2A;  /* fundo da página */
  --color-panel:     #1B4965;  /* painéis, cards de aba */
  --color-accent:    #5FA8D3;  /* bordas de foco, links */
  --color-text:      #CAE9FF;  /* texto principal */
  --color-cta:       #E9C46A;  /* botões primários */
  --color-cta-text:  #0D1B2A;  /* texto sobre botão âmbar */

  --font-display: 'Playfair Display', Georgia, serif;
  --font-body:    'Inter', system-ui, sans-serif;
  --font-data:    'JetBrains Mono', 'Courier New', monospace;

  --radius-sm: 4px;
  --radius-md: 8px;
  --space-sm:  8px;
  --space-md:  16px;
  --space-lg:  32px;
}
```

### Estrutura geral da página

```
┌────────────────────────────────────────────────────────────────┐
│                        FAIXA TOPO                              │
│   FROM: VOCÊ  ✈  TO: QUALQUER LUGAR                           │
│   font: Playfair Display italic · cor: #E9C46A · bg: #0D1B2A  │
│   padding: 24px 40px · text-align: center · letter-spacing: 4px│
├────────────────────────────────────────────────────────────────┤
│  BARRA DE ABAS (gr.Tabs)                                       │
│  [ Clientes ]  [ Destinos ]  [ Vendas ]  [ Comentários ]       │
│  ↑ aba ativa: underline 2px #E9C46A, texto #E9C46A            │
│  ↑ aba inativa: texto #CAE9FF opacity 0.6                     │
├────────────────────────────────────────────────────────────────┤
│  CONTEÚDO DA ABA (fundo #1B4965, border-radius 8px)           │
│  padding: 32px 40px                                            │
│                                                                │
│  ┌─── COLUNA ESQUERDA (40%) ───┐  ┌─── COLUNA DIREITA (58%) ─┐│
│  │  FORMULÁRIO                 │  │  PAINEL DE RESULTADO      ││
│  │  (inputs + botão CTA)       │  │  (mensagem de status ou   ││
│  │                             │  │   tabela de dados)        ││
│  └─────────────────────────────┘  └───────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Aba Clientes

```
COLUNA ESQUERDA — Formulário
─────────────────────────────
Label: "Nome do viajante"          font-body 13px #CAE9FF
Input: gr.Textbox                  bg #0D1B2A, border 1px #5FA8D3,
                                   placeholder: "ex: Maria Silva"
Label: "E-mail de contato"
Input: gr.Textbox                  placeholder: "ex: maria@email.com"

[ Cadastrar Cliente ]              bg #E9C46A, text #0D1B2A, bold,
                                   border-radius 4px, width 100%

COLUNA DIREITA — Status
─────────────────────────
• Estado inicial: vazio (sem texto)
• Sucesso: "✓ Cliente cadastrado com sucesso."
           cor #5FA8D3, font-body 14px
• Erro:    "✗ Erro: [mensagem do banco]"
           cor #E9C46A, font-body 14px
```

### Aba Destinos

```
COLUNA ESQUERDA — Formulário
─────────────────────────────
Label: "Nome do destino"
Input: gr.Textbox                  placeholder: "ex: Lisboa"
Label: "País"
Input: gr.Textbox                  placeholder: "ex: Portugal"
Label: "Preço (R$)"
Input: gr.Number                   min=0, precision=2

[ Cadastrar Destino ]              mesmo estilo CTA âmbar

COLUNA DIREITA — Status
─────────────────────────
• Mesmo padrão de sucesso/erro da aba Clientes
```

### Aba Vendas

```
COLUNA ESQUERDA — Formulário
─────────────────────────────
Label: "Cliente"
Dropdown: gr.Dropdown              choices=listar_clientes() → ["id – Nome"]
                                   bg #0D1B2A, accent #5FA8D3
Label: "Destino"
Dropdown: gr.Dropdown              choices=listar_destinos() → ["id – Nome (País)"]
Label: "Data da viagem"
Input: gr.Textbox                  placeholder: "AAAA-MM-DD"
                                   (gr.DatePicker se disponível na versão Gradio)

[ Registrar Venda ]                mesmo estilo CTA âmbar

COLUNA DIREITA — Status
─────────────────────────
• Sucesso: "✓ Venda registrada para [Nome Cliente] → [Nome Destino]."
• Erro:    "✗ Erro: cliente ou destino inválido."
```

### Aba Comentários

```
COLUNA ESQUERDA — Formulário
─────────────────────────────
Label: "Quem está avaliando?"
Dropdown: gr.Dropdown              choices=listar_clientes()
Label: "Destino visitado"
Dropdown: gr.Dropdown              choices=listar_destinos()
Label: "Sua avaliação"
Input: gr.Textbox                  lines=4, max_lines=8
                                   placeholder: "Conte como foi a viagem..."

[ Enviar Comentário ]              CTA âmbar

COLUNA DIREITA — Tabela de comentários
───────────────────────────────────────
[ Ver Todos os Comentários ]       botão secundário: border 1px #5FA8D3,
                                   bg transparente, text #CAE9FF

Tabela: gr.Dataframe               colunas: Cliente | Destino | Comentário | Data
                                   bg #0D1B2A, header bg #1B4965
                                   font-data para IDs, font-body para texto

Estado vazio (antes de clicar):
  Texto: "Nenhum comentário ainda. Seja o primeiro a avaliar uma viagem."
  font-body italic, #CAE9FF opacity 0.6, text-align center
```

### Elemento Assinatura

A faixa de topo `FROM: VOCÊ · ✈ · TO: QUALQUER LUGAR` em `Playfair Display` itálico, `letter-spacing: 4px`, cor `#E9C46A` sobre `#0D1B2A`. Aparece **uma única vez**, no topo — é o único elemento com personalidade explícita; tudo ao redor é disciplinado e contido.

### Regras de copy dos componentes

| Elemento | Texto |
|---|---|
| Botão principal — Clientes | "Cadastrar Cliente" |
| Botão principal — Destinos | "Cadastrar Destino" |
| Botão principal — Vendas | "Registrar Venda" |
| Botão principal — Comentários | "Enviar Comentário" |
| Botão listagem | "Ver Todos os Comentários" |
| Sucesso genérico | "✓ [Entidade] [verbo no passado] com sucesso." |
| Erro genérico | "✗ Erro: [mensagem técnica direta]" |
| Tela vazia de tabela | "Nenhum comentário ainda. Seja o primeiro a avaliar uma viagem." |

## Testing Decisions

- Testes automatizados de interface Gradio são complexos; o foco de testes estará nos repositórios (Spec 02).
- Verificação manual: rodar a aplicação localmente e executar o fluxo completo: cadastrar cliente → destino → venda → comentário → ver comentários.
- Verificar no Supabase Dashboard que os registros foram inseridos corretamente.
- Verificar no MongoDB Atlas que os documentos de comentários foram inseridos.

## Tasks

- [ ] Adicionar dependência `gradio` ao `pyproject.toml`
- [ ] Criar `src/ds_unicamp_applicada_3/app_gradio.py` com estrutura `gr.Blocks` e abas
- [ ] Implementar aba "Clientes" com formulário de cadastro e callback
- [ ] Implementar aba "Destinos" com formulário de cadastro e callback
- [ ] Implementar aba "Vendas" com dropdowns de cliente/destino, campo de data e callback
- [ ] Implementar aba "Comentários" com dropdown de cliente/destino, textarea de texto, botão de envio e botão "Ver Comentários" com exibição em tabela
- [ ] Testar o fluxo completo manualmente
- [ ] Registrar o comando de execução no `README.md` (ex: `uv run gradio src/.../app_gradio.py`)

## Out of Scope

- Autenticação/login de usuários.
- Edição ou exclusão de registros via interface Gradio (somente Create e Read).
- Update dinâmico dos dropdowns ao cadastrar novos itens sem recarregar a página.
- Deploy em produção (Hugging Face Spaces, etc.).

## Further Notes

- Esta spec depende da Spec 02 (repositórios) estar concluída.
- O Gradio roda em `http://localhost:7860` por padrão; não há conflito com o Tkinter (processo separado).
- Manter os callbacks simples: recebem strings dos inputs → chamam repositório → retornam string de status.
