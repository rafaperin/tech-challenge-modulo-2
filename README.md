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

# Infraestrutura

Este repositório contém os arquivos de configuração e implantação para um aplicativo e banco de dados no diretório `kubernetes`. Os comandos e arquivos Kubernetes a seguir são usados para implantar e gerenciar esses recursos no cluster Kubernetes.

## Implantação do Aplicativo

Os seguintes comandos são usados para implantar o aplicativo:

```bash
kubectl apply -f .\tech-challenge-app-config.yaml
kubectl apply -f .\tech-challenge-app-deployment.yaml
kubectl apply -f .\tech-challenge-app-service.yaml
```
- tech-challenge-app-config.yaml - *Arquivo de configuração do aplicativo.*
- tech-challenge-app-deployment.yaml - *Configuração de implantação do aplicativo.*
- tech-challenge-app-service.yaml - *Configuração do serviço do aplicativo.*

## Implantação do Banco de Dados

```bash
kubectl apply -f .\tech-challenge-secret.yaml
kubectl apply -f .\tech-challenge-db-deployment.yaml
kubectl apply -f .\tech-challenge-db-persistent-volume.yaml
kubectl apply -f .\tech-challenge-db-persistent-volume-claim.yaml
kubectl apply -f .\tech-challenge-db-storage-class.yaml
kubectl apply -f .\tech-challenge-db-service.yaml
```
- tech-challenge-db-deployment.yaml - *Configuração de implantação do banco de dados.*
- tech-challenge-db-persistent-volume.yaml - *Configuração do volume persistente do banco de dados.*
- tech-challenge-db-persistent-volume-claim.yaml - *Configuração do pedido de volume persistente do banco de dados.*
- tech-challenge-db-storage-class.yaml - *Classe de armazenamento para o banco de dados.*
- tech-challenge-db-service.yaml - *Configuração do serviço do banco de dados.*

## Secret

```bash
kubectl apply -f .\tech-challenge-secret.yaml
```

- tech-challenge-secret.yaml - *Configuração do segredo.*

## Implantação de Todos os Recursos

Para implantar todos os recursos do aplicativo e do banco de dados, você pode usar o seguinte comando:

```bash
kubectl apply -f .
```

## Comandos Úteis

`kubectl get pods` - *Obter a lista de pods em execução no cluster.*
`kubectl delete --all pods,deployments,configmaps,services,pv,pvc,storageclass,secrets` - *Excluir todos os pods, implantações, configurações, serviços, volumes persistentes, pedidos de volume persistente, classes de armazenamento no cluster e secrets.*