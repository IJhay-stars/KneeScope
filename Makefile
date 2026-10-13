.PHONY: setup api test lint format up

setup:
	pip install -e ".[dev]" && pre-commit install

api:
	uvicorn knee_api.main:app --reload --port 8000

test:
	pytest

lint:
	ruff check . && ruff format --check . && mypy src

format:
	ruff check --fix . && ruff format .

up:
	docker compose up --build
