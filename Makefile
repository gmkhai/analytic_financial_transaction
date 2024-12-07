
create-network:
	@echo 'create docker network...'
	@docker network create -d bridge final_test
	@echo 'docker network created!!!'

docker-build:
	@echo 'create docker build...'
	@docker build -t final-project/spark -f ./spark/dockers/Dockerfile.spark .
	@echo '__________________________________________________________'
	@docker build -t final-project/airflow -f ./airflow/dockers/Dockerfile.airflow .
	@echo '__________________________________________________________'
	@docker build -t final-project/fastapi -f ./fast_api/dockers/Dockerfile.fastapi .
	@echo '__________________________________________________________'
	@docker build -t final-project/dbt -f ./data_build_tools/dockers/Dockerfile.dbt .
	@echo '==========================================================='
	@echo 'docker build success!!!'


docker-compose:
	@echo 'create docker build...'
	@docker compose -f dockers/docker-compose/docker-compose-postgres.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f spark/dockers/docker-compose-spark.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f airflow/dockers/docker-compose-airflow.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f fast_apidockers/docker-compose-fastapi.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f data_build_tools/dockers/docker-compose-dbt.yml --env-file .env up -d
	@echo '__________________________________________________________'
	@docker compose -f dockers/docker-compose/docker-compose-minio.yml --env-file .env up -d
	@echo '==========================================================='
	@echo 'created docker container success!!!'
