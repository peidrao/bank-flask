DOCKER_COMPOSE=docker-compose 
DOCKER_DATABASE=bank_db
FLASK=flask

docker.up:
	$(DOCKER_COMPOSE) up -d

docker.build:
	$(DOCKER_COMPOSE) up -d --build

flask.run:
	$(FLASK) run --host=0.0.0.0 --debug

db.migrate:
	flask db upgrade

fmt:
	ruff check . --fix
	ruff format .

populate.create_superuser:
	python manage.py createsuperuser

test:
	pytest