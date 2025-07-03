.PHONY: help lint format clean test install update

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: ## Run pre-commit checks on all files
	poetry run pre-commit run --all-files

format: ## Format code with black and ruff
	poetry run black .
	poetry run ruff check --fix .

clean: ## Clean up Python artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	rm -rf build/ dist/

test: ## Run tests
	poetry run pytest

install: ## Install dependencies with Poetry
	pip install --upgrade pip
	pip install poetry==2.1.3
	poetry install
	poetry run pip install pre-commit
	poetry run pre-commit install

update: ## Update dependencies with Poetry
	poetry update
	pre-commit autoupdate
