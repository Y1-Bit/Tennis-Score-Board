.PHONY: build up down logs test clean

DOCKER_COMPOSE = docker-compose

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

test:
	$(DOCKER_COMPOSE) run --rm web poetry run pytest

clean:
	docker system prune -f

migrate:
	$(DOCKER_COMPOSE) run --rm web poetry run alembic upgrade head

makemigrations:
	@read -p "Enter migration message: " message; \
	$(DOCKER_COMPOSE) run --rm web poetry run alembic revision --autogenerate -m "$$message"

shell:
	$(DOCKER_COMPOSE) exec web /bin/bash

install:
	poetry install

update:
	poetry update

lint:
	poetry run flake8 .

format:
	poetry run black .

typecheck:
	poetry run mypy .