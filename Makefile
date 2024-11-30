
create-network:
	@echo 'create docker network...'
	@docker network create -d bridge final_test
	@echo 'docker created!!!'

docker-build:
	@docker build -t final-project/spark -f ./docker/Dockerfile/Dockerfile-spark .
	@echo '__________________________________________________________'
	@docker build -t final-project/airflow -f ./docker/Dockerfile/Dockerfile-airflow .
	@echo '__________________________________________________________'
	@docker build -t final-project/fastapi -f ./docker/Dockerfile/Dockerfile-fastapi .
	@echo '__________________________________________________________'
	@docker build -t final-project/dbt -f ./docker/Dockerfile/Dockerfile-dbt .
	@echo '==========================================================='

docker-compose:
