.PHONY: install test cov check format format-check generate

install:
	uv sync

test:
	uv run pytest

cov:
	uv run pytest --cov --cov-report=term-missing

check:
	uv run ruff check .

format:
	uv run ruff check --fix .
	uv run ruff format .

format-check:
	uv run ruff check .
	uv run ruff format --check .

generate:
	uv run python bin/generate.py
	uv run ruff check --fix linear_python_client/
	uv run ruff format linear_python_client/
