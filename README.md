# Backend API

Servidor do backend da API

# Conteúdo
   * [Setup banco de dados](#setup-banco-de-dados)
      * [Instala banco de dados](#instala-banco-de-dados)
   * [Setup ambiente de desenvolvimento](#setup-ambiente-de-desenvolvimento)
      * [Instala a aplicação](#instala-a-aplicacao)
      * [Cria ambiente virtual python](#cria-ambiente-virtual-python)
      * [Instala pacotes python](#instala-pacotes-python)
      * [Rodando servidor no ambiente local](#rodando-servidor-no-ambiente-local)
    * [Rodando testes no ambiente local](#rodando-testes-no-ambiente-local)
   * [Referências](#referências)

# Setup banco de dados

## Instala banco de dados

Instalar (linux):

    sudo apt-get install postgresql

No linux o serviço postgresql já começa rodando logo após instalar. Você pode checar se está rodando com:

    service postgresql status

E no linux caso não esteja rodando, inicie com:

    service postgresql start

Criar usuários e bancos locais de desenvolvimento e testes:

    dropdb api_dev;
    dropdb api_test;
    createuser api_dev_user;
    createuser api_test_user;
    createdb -Oapi_dev_user -Eutf8 api_dev;
    createdb -Oapi_test_user -Eutf8 api_test;

# Setup ambiente de desenvolvimento

## Instala a aplicação

Dentro de uma pasta, onde deseja instalar o projeto:

    git clone git@github.com:danilolmoura/desafio-backend.git

Após o download, entrar na pasta do projeto:

    cd desafio-backend/

## Cria ambiente virtual python

    sudo apt-get install -y python-pip
    sudo pip install -U virtualenv

    python -m venv venv (Utilizar python 3.7)

    source venv/bin/activate
    pip install --upgrade pip

## Instala pacotes python

    source venv/bin/activate (caso já não esteja ativado)
    pip install -r requirements.txt

## Rodando servidor no ambiente local

Aplicar migrations no banco de dados de desenvolvimento local

    alembic upgrade head

Para rodar o ambiente local, devemos definir as variáveis de ambiente abaixo

    export USERNAME_API_DEV=api_dev_user
    export PASSWORD_API_DEV=<SEU_PASSWORD>
    export HOST_API_DEV=localhost
    export DATABASE_API_DEV=api_dev

E em seguida executar o comando abaixo

    python app.py

A aplicação está disponível em http://localhost:5000/

## Rodando testes no ambiente local

Para rodar os testes unitários, devemos definir as variáveis de ambiente abaixo

    export USERNAME_API_TEST=api_test_user
    export PASSWORD_API_TEST=<SEU_PASSWORD>
    export HOST_API_TEST=localhost
    export DATABASE_API_TEST=api_test

Aplicar migrations no banco de dados de teste

    cp alembic_test.ini alembic.ini
    alembic upgrade head
    git checkout alembic.ini

E em seguida executar o comando abaixo

    pytest tests/funcional/

# Referências

* [Documentação Flask](http://flask.palletsprojects.com/en/1.1.x/)
* [Documentação Flask JWT](https://pythonhosted.org/Flask-JWT/)
* [Documentação Flask Potion](https://potion.readthedocs.io/en/latest/)
* [Documentação SQLAlchemy](https://docs.sqlalchemy.org/en/13/)
