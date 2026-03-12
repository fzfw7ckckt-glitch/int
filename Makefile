.PHONY: help build up down logs restart clean test lint security-check

help:
	@echo "OSINT Platform 2026 - Docker Commands"
	@echo "====================================="
	@echo "make setup          - Initial setup and build"
	@echo "make build          - Build all Docker images"
	@echo "make up             - Start all services"
	@echo "make down           - Stop all services"
	@echo "make restart        - Restart all services"
	@echo "make logs           - View logs for all services"
	@echo "make logs-api       - View API logs"
	@echo "make logs-worker    - View Worker logs"
	@echo "make logs-web       - View Web logs"
	@echo "make ps             - Show running containers"
	@echo "make clean          - Stop and remove containers, volumes"
	@echo "make test           - Run tests"
	@echo "make lint           - Run linters"
	@echo "make shell-api      - Open shell in API container"
	@echo "make shell-worker   - Open shell in Worker container"
	@echo "make db-init        - Initialize database"
	@echo "make db-migrate     - Run Alembic migrations"
	@echo "make stats          - Show resource usage"
	@echo "make security-check - Run security checks"

setup:
	@bash docker-setup.sh

build:
	docker-compose build --no-cache

up:
	docker-compose up -d
	@echo "✅ Services started. Wait 10 seconds for services to be ready..."
	@sleep 10
	@make ps

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-worker:
	docker-compose logs -f worker

logs-web:
	docker-compose logs -f web

ps:
	docker-compose ps

clean:
	docker-compose down -v --remove-orphans
	rm -rf reports/* 2>/dev/null || true
	@echo "✅ Clean complete"

test:
	docker-compose run --rm api pytest tests/ -v --cov=app

lint:
	docker-compose run --rm api bash -c "ruff check . && mypy app/"

shell-api:
	docker-compose exec api bash

shell-worker:
	docker-compose exec worker bash

db-init:
	docker-compose exec api python scripts/init_db.py

db-migrate:
	docker-compose exec api alembic upgrade head

stats:
	docker stats

security-check:
	docker-compose run --rm api pip-audit
	@echo "✅ Security check complete"

pull:
	docker-compose pull

push:
	@echo "Pushing images to registry (configure in docker-compose.yml)"
	docker image push osint-platform:api
	docker image push osint-platform:worker
	docker image push osint-platform:web

health-check:
	@echo "Checking service health..."
	@docker-compose exec api curl -s http://localhost:8000/health
	@echo "\n✅ API is healthy"
	@docker-compose exec redis redis-cli ping
	@echo "✅ Redis is healthy"
	@docker-compose exec postgres pg_isready -U osint
	@echo "✅ PostgreSQL is healthy"
