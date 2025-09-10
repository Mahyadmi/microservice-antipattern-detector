.PHONY: help setup build up down clean test logs status restart

help:
	@echo "Available commands:"
	@echo "  make setup   - Initial setup"
	@echo "  make build   - Build Docker images"
	@echo "  make up      - Start all services"
	@echo "  make down    - Stop all services"
	@echo "  make clean   - Clean up volumes"
	@echo "  make test    - Run tests"
	@echo "  make logs    - View logs"
	@echo "  make status  - Check service status"
	@echo "  make restart - Restart all services"

setup:
	chmod +x scripts/*.sh
	./scripts/setup.sh

build:
	docker-compose build --no-cache

up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 30
	@echo "Services ready!"
	@echo "API: http://localhost:8000"
	@echo "Dashboard: http://localhost:3000"
	@echo "SonarQube: http://localhost:9002"
	@echo "MinIO: http://localhost:9001"

down:
	docker-compose down

clean:
	docker-compose down -v
	rm -rf test-projects/uploads

test:
	./scripts/test.sh

logs:
	docker-compose logs -f

status:
	docker-compose ps

restart: down up
