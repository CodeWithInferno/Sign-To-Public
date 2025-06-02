.PHONY: install test lint clean run-server run-ui

# Installation
install:
	pip install -r requirements.txt

# Install in development mode
install-dev: install
	pip install -e .

# Install UI dependencies
install-ui:
	cd UI_expo && npm install

# Run tests
test:
	pytest

# Code formatting and linting
lint:
	black .
	flake8 .
	isort .

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +

# Run server
run-server:
	python server/App.py

# Run UI in development
run-ui:
	cd UI_expo && npm start

# Train model
train:
	python Scripts/train/train.py

# Run live testing
test-live:
	python Scripts/train/test_live.py

# Help
help:
	@echo "Available commands:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make install-dev  - Install in development mode"
	@echo "  make install-ui   - Install UI dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run code formatting and linting"
	@echo "  make clean        - Clean up generated files"
	@echo "  make run-server   - Start the server"
	@echo "  make run-ui       - Start the UI in development mode"
	@echo "  make train        - Train the model"
	@echo "  make test-live    - Run live testing"
	@echo "  make help         - Show this help message"