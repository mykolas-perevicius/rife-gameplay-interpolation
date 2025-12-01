.PHONY: help install dev setup test lint format clean run

PYTHON := python
VENV := venv

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

dev:  ## Install dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"
	pre-commit install

setup:  ## Download models and setup environment
	$(PYTHON) -m src.cli setup

test:  ## Run tests
	pytest tests/ -v --cov=src

lint:  ## Run linting
	ruff check src/
	black --check src/

format:  ## Format code
	black src/
	isort src/

clean:  ## Clean temporary files
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -rf dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

run:  ## Run CLI (example: make run ARGS="interpolate -h")
	$(PYTHON) -m src.cli $(ARGS)

interpolate:  ## Quick interpolate (make interpolate IN=video.mp4 OUT=out.mp4)
	$(PYTHON) -m src.cli interpolate $(IN) $(OUT)

benchmark:  ## Run benchmark (make benchmark IN=video.mp4)
	$(PYTHON) -m src.cli benchmark $(IN)
