# Makefile

# Define variables (optional)
PYTHON := python
CELERY := celery -A tasks worker --loglevel=info
FLASK := flask run
INSTALL := poetry install

# Default target
.PHONY: all
all: help

# Target for running and gracefull shutdown of the Celery worker
.PHONY: run-celery celery-stop
run-celery:
    celery -A tasks worker --loglevel=info

celery-stop:
    pkill -f 'celery worker'  # Use a gentle shutdown command

# Target for running the Flask server
.PHONY: run-flask
run-flask:
	$(FLASK)

# Target for running the RabbitMQ listener
.PHONY: run-listener
run-listener:
	python rabbit_listener.py

# Target for installing dependencies
.PHONY: install
install:
	$(INSTALL)

# Target to clean up any __pycache__ or temporary files
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

# Help target to display available commands
.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  run-celery      Start the Celery worker with log level info"
	@echo "  run-flask       Start the Flask development server"
	@echo "  install         Install dependencies with Poetry"
	@echo "  clean           Remove temporary files like __pycache__"
