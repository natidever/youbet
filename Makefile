build:
	docker compose build
up:
	docker compose up --watch
down:
	docker compose down
db_push:
	docker compose exec backend alembic upgrade head
test:
	python -m pytest app/test -p no:warnings
# db_commit:
# 	docker compose exec backend alembic revision --autogenerate -m "$(comment)"

# comment = minor change
db_commit:
	docker compose exec backend alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

# Ignore the message argument from being interpreted as a target
%:
	@:


up_prod:
	docker-compose up 
down_prod:
	docker-compose down
