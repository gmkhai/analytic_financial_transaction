docker-build:
	@docker build -t final-project/spark -f ./docker-compose/Dockerfile/Dockerfile-spark .
	@echo '__________________________________________________________'
	@docker build -t final-project/airflow -f ./docker-compose/Dockerfile/Dockerfile-airflow .
	@echo '__________________________________________________________'
	@docker build -t final-project/fastapi -f ./docker-compose/Dockerfile/Dockerfile-fastapi .
	@echo '__________________________________________________________'
	@docker build -t final-project/dbt -f ./docker-compose/Dockerfile/Dockerfile-dbt .
	@echo '==========================================================='