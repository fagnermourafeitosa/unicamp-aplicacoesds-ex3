Tarefa Aula 3 — Agência de Viagens: Cadastro e Comentários

Contexto geral

A tarefa propõe o desenvolvimento de uma aplicação web simples, construída com
Python e a biblioteca Gradio (usada para criar interfaces de usuário de forma rápida e
visual, sem necessidade de HTML/CSS/JS), além de uma segunda aplicação, desktop,
construída com Tkinter, para administração completa dos dados. Juntas, as duas
aplicações simulam o sistema de uma agência de viagens, permiƟndo o cadastro de
clientes, desƟnos, vendas e comentários sobre as viagens realizadas.
O diferencial da tarefa está no uso de dois bancos de dados diferentes ao mesmo
tempo, cada um responsável por um Ɵpo de informação:
 Supabase (PostgreSQL) — banco relacional, usado para os dados estruturados e
transacionais (clientes, desƟnos e vendas).
 MongoDB Atlas — banco não-relacional (NoSQL, orientado a documentos),
usado para os comentários dos clientes, que são dados mais livres e textuais.
Isso faz da tarefa um exercício de integração poliglota de persistência (usar bancos
relacionais e não-relacionais dentro da mesma aplicação), além de praƟcar a construção
de duas interfaces disƟntas — uma web (Gradio) e uma desktop (Tkinter) — operando
sobre a mesma base de dados.

Estrutura de dados
No Supabase (banco relacional PostgreSQL), três tabelas:
 clientes: id, nome, email
 desƟnos: id, nome, país, preço
 vendas: id, cliente_id, desƟno_id, data_viagem
A tabela vendas funciona como uma tabela associaƟva, relacionando um cliente a um
desƟno através de chaves estrangeiras (cliente_id e desƟno_id), além de registrar a data
da viagem — um modelo clássico de banco relacional normalizado.
No MongoDB Atlas (banco não-relacional), uma coleção:
 comentarios: cliente_id, desƟno_id, texto, data
Aqui os dados não seguem uma estrutura rígida de tabelas com chaves estrangeiras
formais como no modelo relacional — é um documento (semelhante a um JSON) que

referencia o cliente e o desƟno, mas armazenado de forma mais flexível, ơpica do
MongoDB.

Parte 1 — Aplicação web em Gradio
ObjeƟvo: permiƟr o cadastro de clientes, desƟnos e vendas (gravados no Supabase) e o
cadastro/visualização de comentários dos clientes sobre as viagens (gravados no
MongoDB Atlas).
Funcionalidades esperadas:
1. Cadastro de clientes, desƟnos e vendas, através de campos de entrada (inputs)
simples — nome, email, desƟno, data — que gravam os dados no Supabase ao
serem submeƟdos.
2. Cadastro de comentários: um campo de input de texto livre onde o cliente
escreve seu comentário sobre a viagem, vinculado ao cliente e ao desƟno. Esse
comentário é enviado e salvo na coleção comentarios do MongoDB Atlas.
3. Visualização dos comentários: a aplicação deve oferecer uma função para
consultar o MongoDB Atlas e exibir na tela, em lista ou tabela, todos os
comentários já cadastrados.
Fluxo esperado: o usuário acessa a interface → cadastra um cliente → cadastra um
desƟno → registra uma venda vinculando cliente + desƟno + data → escreve um
comentário sobre a viagem → clica em "ver comentários" e visualiza tudo o que já foi
cadastrado.

Parte 2 — Interface CRUD em Tkinter
Além da aplicação web, os alunos deverão construir uma segunda interface, agora
desktop, uƟlizando a biblioteca Tkinter do Python. Essa interface terá como objeƟvo
permiƟr a administração completa dos dados cadastrados no Supabase, oferecendo as
quatro operações fundamentais de um sistema de gerenciamento: Create, Read, Update
e Delete (CRUD).
Funcionalidades esperadas:
1. Cadastrar (Create) — inserir novos registros de clientes, desƟnos e vendas,
através de formulários (campos Entry) correspondentes às colunas de cada
tabela.
2. Consultar (Read) — listar todos os registros existentes em uma tabela visual
(Ʃk.Treeview), permiƟndo a visualização direta dos dados na tela.

3. Atualizar (Update) — ao selecionar um registro na listagem, seus dados devem
ser carregados nos campos de edição, possibilitando alterar as informações e
salvar a atualização no banco.
4. Excluir (Delete) — remover o registro selecionado do banco de dados,
preferencialmente com uma confirmação antes da exclusão definiƟva.
A tela deve conter botões de ação claros para cada operação — "Cadastrar", "Atualizar",
"Excluir" e "Atualizar Lista" — e, idealmente, usar abas (Notebook) para separar o
gerenciamento de clientes, desƟnos e vendas dentro da mesma janela.
Requisito técnico: a aplicação Tkinter deve se conectar ao mesmo banco Supabase
(PostgreSQL) uƟlizado na aplicação Gradio, reaproveitando a mesma estrutura de
tabelas (clientes, desƟnos, vendas), reforçando a ideia de que diferentes interfaces (web
e desktop) podem operar sobre a mesma base de dados.

O que essa tarefa está avaliando, na práƟca
 Capacidade de configurar e conectar duas bases de dados na nuvem (Supabase
e MongoDB Atlas) a parƟr de aplicações Python.
 Compreensão da diferença entre modelagem relacional (tabelas, chaves
primárias/estrangeiras) e modelagem não-relacional (documentos, coleções).
 Construção de uma interface web funcional com Gradio e de uma interface
desktop funcional com Tkinter, ambas com formulários de entrada e exibição de
resultados.
 Implementação do ciclo completo de CRUD — Create e Read na aplicação Gradio;
Create, Read, Update e Delete na aplicação Tkinter — distribuído entre dois
bancos diferentes, simulando um cenário real onde diferentes Ɵpos de dados são
armazenados nos bancos mais adequados às suas caracterísƟcas, e onde
diferentes públicos (usuário final vs. administrador) usam interfaces disƟntas
para o mesmo sistema.