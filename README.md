
# Python Flask API - Sistema de Gestão de Mercadorias da MStarSupply

Esta API oferece autenticação por JWT (Bearer Token) e funcionalidades completas de gestão de usuários e gestão de mercadorias com operações de cadastros das mercadorias, as entradas e saídas.

Considere executar as primeiras requisições com pelo menos com 1 superuser já inserido no Banco de Dados para gerar o Token.
## Documentação da API

* [Documentação Postman](https://documenter.getpostman.com/view/31811666/2s9YsQ6ooN#07cf2261-cc59-4bf8-bcdb-7bfc11596d42)


# Instalação

#### Criando Banco de Dados
Esta ação considera um BD MySQL executando num container Docker, mas você pode utilizar outro ambiente de sua preferência.

* MySQL no Docker

```bash
  cd my-api-folder
  docker build -t mstar-supply-api .
  docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=RootPassword -e MYSQL_DATABASE=mssupply_goods_api -e MYSQL_USER=MainUser -e MYSQL_PASSWORD=MainPassword mstar-supply-api
```
#### Preparando ambiente Python
* Criando Ambiente Virtual da API
```bash
  cd my-api-folder
  python -m venv venv
  cd venv/scripts
  .\activate
  cd ../..
```
* Instalando dependências
```bash
  pip install -r requirements.txt  
``` 
* Se necessário, modifique o arquivo **config_db.py** com as informações do seu servidor de banco de dados.

* Executando API Server
```bash
  python main.py
``` 


## Stack utilizada

**Back-end:** API Python Flask, MySQL, Docker
