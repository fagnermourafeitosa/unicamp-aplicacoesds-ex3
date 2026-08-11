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
