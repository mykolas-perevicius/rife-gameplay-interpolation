# Contributing

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
```bash
pip install -e ".[dev]"
pre-commit install
```

## Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **isort** for import sorting

Run formatters:
```bash
make format
```

Run linters:
```bash
make lint
```

## Testing

Run the test suite:
```bash
make test
```

Or with coverage:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Reporting Issues

Please include:
- Python version
- GPU model and driver version
- Steps to reproduce
- Expected vs actual behavior
