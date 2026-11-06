# Controle de EPI (SafeStock)

Projeto da Situação de Aprendizagem VI (Senai, Técnico em Desenvolvimento de Sistemas).
Sistema de gerenciamento de EPIs para uma empresa do setor têxtil (Django + SQLite + Bootstrap).
Além do CRUD de **colaboradores**, **equipamentos** e **empréstimos**, esta etapa implementa a
**autenticação e o controle de acesso** do sistema.

## Funcionalidades

### Autenticação e controle de acesso

- **Login** (`/auth/`): tela com usuário e senha. Se os dados estiverem errados, mostra uma mensagem de erro; se estiverem certos, abre a página inicial.
- **Logout**: o botão **Sair** do menu lateral encerra a sessão e volta para a tela de login.
- **Rotas protegidas**: todas as rotas exigem login, **exceto** o login e o logout (`/auth/...`) e o `/admin/` (que tem a tela de login própria do Django). Quem tentar abrir qualquer outra página sem estar logado é redirecionado para `/auth/?next=<página>`.
- **Usuário logado**: o nome do usuário aparece no canto direito da barra superior (nome completo, ou o nome de usuário se o nome não estiver preenchido).
- **Controle de usuários e grupos pelo django admin** (`/admin/`): é possível criar grupos, definir as permissões de cada grupo (adicionar, alterar, visualizar e excluir dados de um model) e colocar usuários nesses grupos. Hoje o model registrado no admin é **Categoria de EPI**.

### Colaboradores

- **Listar** colaboradores, com **pesquisa por nome** e mensagem quando não há resultados.
- **Cadastrar** (`/criar`): mostra mensagem de sucesso/falha e **permanece na tela de cadastro**.
- **Editar** (`/editar/<id>`): tela parecida com a de cadastro, já preenchida com os dados atuais.
- **Excluir**: abre um modal pedindo confirmação antes de remover.

### Equipamentos (EPIs)

- **Listar** com **pesquisa por nome**, **cadastrar** (nome, categoria e tamanho), **editar** e **excluir**.
- As categorias iniciais são criadas pelas migrações e podem ser gerenciadas pelo admin.

### Empréstimos

- **Cadastrar** (`/criar-emprestimo`): colaborador, equipamento, data prevista de devolução (precisa ser futura), status (Emprestado ou Fornecido) e condições do equipamento.
- **Listar** (`/emprestimo-home`) com filtros por colaborador, equipamento e status, **combinados** (todos os filtros preenchidos precisam ser atendidos).
- **Editar**: atualiza status, condições, data da devolução e observação. Colaborador, equipamento e datas do empréstimo não podem ser alterados. Ao marcar *Devolvido*, *Danificado* ou *Perdido*, a data da devolução é obrigatória.

Os dados ficam salvos no arquivo `db.sqlite3`, então continuam lá depois de parar e iniciar a aplicação.

## Como executar

Pré-requisitos: Python 3.10+ e pip.

```bash
# 1. (opcional) criar e ativar um ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

# 2. instalar as dependências
pip install -r requirements.txt

# 3. criar/atualizar as tabelas do banco
python manage.py migrate

# 4. iniciar o servidor
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ — como o sistema exige login, você será levado para a tela de login (`/auth/`).

> O Bootstrap é carregado por CDN, então é preciso ter internet para a aparência completa.

## Acesso ao sistema

O `db.sqlite3` do repositório já traz um grupo e um usuário de teste:

| Item | Valor |
|------|-------|
| Grupo | `Administradores` (adicionar, alterar, visualizar e excluir nos models do app `nucleo`) |
| Usuário de teste | `YanLucas` (membro do grupo e da equipe, sem ser superusuário) |
| Senha | informada ao professor na entrega |

Esse usuário entra no sistema por `/auth/` e também no admin por `/admin/`, onde enxerga apenas os models do `nucleo` (não vê Usuários nem Grupos).

Para começar com um banco novo, crie um superusuário:

```bash
python manage.py createsuperuser
```

### Como criar um grupo com permissões

1. Entre em `/admin/` com um superusuário.
2. Em **Grupos → Adicionar grupo**, dê um nome e escolha as permissões do model (por exemplo, as 4 de *categoria epi*: adicionar, alterar, visualizar e excluir). Salve.
3. Em **Usuários → Adicionar usuário**, crie o usuário e, na tela seguinte, marque **Membro da equipe** (necessário para entrar no admin) e escolha o grupo em **Grupos**.
4. Entre em `/admin/` com esse usuário: ele só consegue fazer o que o grupo permite.

## Testes

```bash
python manage.py test
```

Os testes cobrem o fluxo de empréstimos (cadastro, validações, filtros e edição) e fazem login com um usuário criado no próprio teste, já que todas as rotas exigem autenticação.

## Rotas

| Rota | Método | Ação | Acesso |
|------|--------|------|--------|
| `/auth/` | GET/POST | Tela e envio do login | livre |
| `/auth/logout/` | GET | Encerra a sessão | livre |
| `/admin/` | — | django admin (usuários, grupos e permissões) | login próprio |
| `/` | GET | Lista colaboradores (`?q=nome` pesquisa) | login |
| `/criar` | GET | Tela de cadastro de colaborador | login |
| `/salvar` | POST | Salva novo colaborador | login |
| `/editar/<id>` | GET | Tela de edição do colaborador | login |
| `/atualizar/<id>` | POST | Salva a edição | login |
| `/excluir/<id>` | POST | Remove o colaborador | login |
| `/epi-home` | GET | Lista equipamentos (`?q=nome` pesquisa) | login |
| `/criar-epi` | GET | Tela de cadastro de equipamento | login |
| `/salvar-epi` | POST | Salva novo equipamento | login |
| `/editar-epi/<id>` | GET | Tela de edição do equipamento | login |
| `/atualizar-epi/<id>` | POST | Salva a edição | login |
| `/excluir-epi/<id>` | POST | Remove o equipamento | login |
| `/emprestimo-home` | GET | Lista empréstimos (`?colaborador=`, `?equipamento=`, `?status=`) | login |
| `/criar-emprestimo` | GET | Tela de cadastro de empréstimo | login |
| `/salvar-emprestimo` | POST | Salva novo empréstimo | login |
| `/editar-emprestimo/<id>` | GET | Tela de edição do empréstimo | login |
| `/atualizar-emprestimo/<id>` | POST | Salva a edição | login |

## Docker (opcional)

O `Dockerfile` instala as dependências, aplica as migrações e sobe o servidor.

```bash
docker build -t epi .
docker run -p 8000:8000 epi
```

Para manter os dados mesmo se o contêiner for recriado, monte o arquivo do banco:

```bash
docker run -p 8000:8000 -v "$(pwd)/db.sqlite3:/app/db.sqlite3" epi
```

## Estrutura

```
epi/            configurações do projeto Django (settings, urls)
nucleo/         app principal (models, views, urls, admin, templates, static, tests)
  templates/nucleo/base.html              layout base (menu lateral, nome do usuário e botão Sair)
  templates/nucleo/index.html             colaboradores: listagem + pesquisa + modal de exclusão
  templates/nucleo/index-epi.html         equipamentos: listagem + pesquisa
  templates/nucleo/index-emprestimo.html  empréstimos: listagem + filtros
  templates/nucleo/forms/                 telas de cadastro e edição
system_auth/    autenticação e controle de acesso
  views.py                  login e logout
  urls.py                   rotas /auth/ e /auth/logout/
  middleware.py             exige login em todas as rotas (exceto /auth/ e /admin/)
  templates/index-login.html  tela de login
```
