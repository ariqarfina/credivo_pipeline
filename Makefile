include .env
.PHONY: run-all

run-all: postgres airflow

.PHONY: stop-all

stop-all:
	@docker-compose -f ./docker/docker-compose-airflow.yml stop
	@docker-compose -f ./docker/docker-compose-postgres.yml stop

docker-build-arm:
	@echo '__________________________________________________________'
	@echo 'Building Docker Images ...'
	@echo '__________________________________________________________'
	@docker network inspect credivo-network >/dev/null 2>&1 || docker network create credivo-network
	@echo '__________________________________________________________'
	@docker build -t credivo-data/spark -f ./docker/Dockerfile.spark .
	@echo '__________________________________________________________'
	@docker build -t credivo-data/airflow -f ./docker/Dockerfile.airflow-arm .
	@echo '__________________________________________________________'
	@docker build -t credivo-data/jupyter -f ./docker/Dockerfile.jupyter .
	@echo '==========================================================='

airflow:
	@echo '__________________________________________________________'
	@echo 'Creating Airflow Instance ...'
	@echo '__________________________________________________________'
	@docker-compose -f ./docker/docker-compose-airflow.yml --env-file .env up -d
	@echo '==========================================================='

postgres: postgres-create  

postgres-create:
	@docker-compose -f ./docker/docker-compose-postgres.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@echo 'Postgres container created at port ${POSTGRES_PORT}...'
	@echo '__________________________________________________________'
	@echo 'Postgres Docker Host	: ${POSTGRES_CONTAINER_NAME}' &&\
		echo 'Postgres Account	: ${POSTGRES_USER}' &&\
		echo 'Postgres password	: ${POSTGRES_PASSWORD}' &&\
		echo 'Postgres Db		: credivo'
	@sleep 5
	@echo '==========================================================='
