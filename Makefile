## help: Show this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

## clean: Run ruff linter
.PHONY: clean
clean:
	ruff check --select I --fix backend/
	ruff format backend/

## upgrade: Alembic upgrade head
.PHONY: upgrade
upgrade:
	alembic upgrade head

## migrate: Generate alembic migration only | Usage | make migrate name=<migration_name>
.PHONY: migrate
migrate: upgrade
	@if [ -z "$(name)" ]; then \
		read -p "Enter migration name: " name; \
	fi
	alembic upgrade head
	alembic revision --autogenerate -m "$(name)"

## run: Run python project
.PHONY: run
run:
	poetry run python backend/app/main.py

## redis: Run redis brocker locally with docker(Used for celery)
.PHONY: redis
redis:
	docker run -d --rm --name some-redis -p 6379:6379 redis:latest

## celery: Run celery locally
.PHONY: celery
celery:
	poetry run celery -A backend.app.api.deps.celery_app worker --loglevel=info --pool=solo
