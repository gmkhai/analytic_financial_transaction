
create-network:
	@echo 'create docker network...'
	@docker network create -d bridge final_test
	@echo 'docker network created!!!'

docker-build:
	@echo 'create docker build...'
	@docker build -t final-project/spark -f ./dockers/Dockerfile/Dockerfile.spark .
	@echo '__________________________________________________________'
	@docker build -t final-project/airflow -f ./dockers/Dockerfile/Dockerfile.airflow .
	@echo '__________________________________________________________'
	@docker build -t final-project/fastapi -f ./dockers/Dockerfile/Dockerfile.fastapi .
	@echo '__________________________________________________________'
	@docker build -t final-project/dbt -f ./dockers/Dockerfile/Dockerfile.dbt .
	@echo '==========================================================='
	@echo 'docker build success!!!'


docker-compose:
	@echo 'create docker build...'
	@docker compose -f ./dockers/docker-compose/docker-compose-postgres.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f ./dockers/docker-compose/docker-compose-spark.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f ./dockers/docker-compose/docker-compose-airflow.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f ./dockers/docker-compose/docker-compose-fastapi.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f ./dockers/docker-compose/docker-compose-dbt.yml --env-file .env up -d
	@echo '==========================================================='
	@echo 'created docker container success!!!'
