# Controle de EPI — CRUD de Colaboradores

Projeto da Situação de Aprendizagem VI (Senai, Técnico em Desenvolvimento de Sistemas).
Sistema de gerenciamento de EPIs para uma empresa do setor têxtil. Esta etapa implementa o
**CRUD de colaboradores** seguindo o wireframe do professor (Django + SQLite + Bootstrap).

## Funcionalidades

- **Listar** colaboradores, com **pesquisa por nome** e mensagem quando não há resultados.
- **Cadastrar** (`/criar`): mostra mensagem de sucesso/falha e **permanece na tela de cadastro**.
- **Editar** (`/editar/<id>`): tela parecida com a de cadastro, já preenchida com os dados atuais.
- **Excluir**: abre um modal pedindo confirmação antes de remover.
- Os dados ficam salvos no arquivo `db.sqlite3`, então continuam lá depois de parar e iniciar a aplicação.

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

Acesse http://127.0.0.1:8000/

> O Bootstrap é carregado por CDN, então é preciso ter internet para a aparência completa.

## Testes

```bash
python manage.py test
```

## Rotas

| Rota | Método | Ação |
|------|--------|------|
| `/` | GET | Lista colaboradores (`?q=nome` pesquisa) |
| `/criar` | GET | Tela de cadastro |
| `/salvar` | POST | Salva novo colaborador |
| `/editar/<id>` | GET | Tela de edição |
| `/atualizar/<id>` | POST | Salva a edição |
| `/excluir/<id>` | POST | Remove o colaborador |

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
epi/            configurações do projeto Django
nucleo/         app principal (models, views, urls, templates, static, tests)
  templates/nucleo/base.html        layout base (menu lateral do wireframe)
  templates/nucleo/index.html       listagem + pesquisa + modal de exclusão
  templates/nucleo/forms/           telas de cadastro e edição
```
