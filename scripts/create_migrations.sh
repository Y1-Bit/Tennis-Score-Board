read -p "Enter name of migration: " message
docker-compose exec web alembic revision --autogenerate -m "$message"