# Tech Challenge

Projeto criado com o objetivo de entregar o desafio proposto pelo Curso de Software Architecture FIAP + Alura.

## Autores
- Rafael Perin - RM349501
- Lucas Gabriel - RM349527

## Stack
- Python 3.8.16
- FastAPI
- PostgreSQL 

## Pré-requisitos
Para executar o projeto, é necessário ter instalado:

- [Docker version >= 20.10.7](https://www.docker.com/get-started)
- [Docker-compose version >= 1.29.2](https://docs.docker.com/compose/install/)

## Rodando com docker-compose

1. Clonar o repositório e executar o comando abaixo na raiz do projeto:

```bash
$ docker compose up -d
```

As variáveis de ambiente foram deixadas hardcoded no arquivo docker-compose.yml para simplicidade de execução, dado o fim apenas educacional do projeto.
 
## Rodando FastAPI

Após rodar o docker-compose, executar o seguinte endereço no navegador:

```
http://localhost:8000/docs
```

Caso tenha o desejo de executar a aplicação via Insomnia ou Postman, é possível capturar os dados em http://localhost:8000/openapi.json e transformar em arquivo .json para ser importado.