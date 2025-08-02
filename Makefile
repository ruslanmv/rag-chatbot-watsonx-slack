# Makefile for the RAG Chatbot Project

# Default shell
SHELL := /bin/bash

# Environment setup
VENV_NAME := venv
PYTHON := $(VENV_NAME)/bin/python

.PHONY: help install setup sync import-kb chat clean

help:
	@echo "Commands:"
	@echo "  install/setup    : Creates a virtual environment and installs dependencies."
	@echo "  sync             : Downloads documents from Box and updates the knowledge base YAML."
	@echo "  import-kb        : Imports the knowledge base into watsonx Orchestrate."
	@echo "  chat             : Starts the watsonx Orchestrate chat interface."
	@echo "  clean            : Removes Python cache files."

# Setup the development environment
install setup:
	@echo "Setting up virtual environment..."
	python3 -m venv $(VENV_NAME)
	@echo "Installing dependencies from requirements.txt..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Setup complete. Activate with: source $(VENV_NAME)/bin/activate"

# Run the Box sync script
sync:
	@echo "Syncing documents from Box and updating knowledge base config..."
	$(PYTHON) sync_and_import.py

# Import the knowledge base
import-kb: sync
	@echo "Importing knowledge base..."
	orchestrate knowledge-bases import -f knowledge_base_box.yaml

# Start the chat interface
chat:
	@echo "Starting watsonx Orchestrate chat..."
	orchestrate chat start

# Clean up temporary files
clean:
	@echo "Cleaning up Python cache files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete."

