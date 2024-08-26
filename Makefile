.PHONY: build up down logs test clean migrate makemigrations shell init

DOCKER_COMPOSE = docker-compose

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

clean:
	docker system prune -f

migrate:
	$(DOCKER_COMPOSE) run --rm web alembic upgrade head

makemigrations:
	@read -p "Enter migration message: " message; \
	$(DOCKER_COMPOSE) run --rm web alembic revision --autogenerate -m "$$message"

init_migration:
	$(DOCKER_COMPOSE) run --rm web alembic revision --autogenerate -m "Initial migration"

shell:
	$(DOCKER_COMPOSE) exec web /bin/bash

test:
	$(DOCKER_COMPOSE) run --rm web pytest

init: build
	$(MAKE) build
	$(MAKE) init_migration
	$(MAKE) migrate
	@echo "Initialization complete. You can now run 'make up' to start the application."