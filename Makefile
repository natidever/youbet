build:
	docker compose build
up:
	docker compose up
down:
	docker compose down
db_push:
	docker compose exec backend alembic upgrade head
db_commit:
	docker compose exec backend alembic revision --autogenerate -m "init"