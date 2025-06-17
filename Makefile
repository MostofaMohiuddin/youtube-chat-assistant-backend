# Variables
IMAGE_NAME = youtube-video-qna-backend
DEV_IMAGE = $(IMAGE_NAME):dev
CONTAINER_NAME = $(IMAGE_NAME)-dev
PORT = 7788

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup target
.PHONY: setup
setup: ## Create virtual environment and install dependencies
	@echo "Setting up virtual environment..."
	@poetry config virtualenvs.in-project true
	@poetry install --no-root
	@echo "Virtual environment created and dependencies installed!"

# Development targets
.PHONY: dev
dev: ## Run development server locally with poetry
	@echo "Starting FastAPI development server..."
	@poetry run uvicorn main:app --host 0.0.0.0 --port $(PORT) --reload

.PHONY: build-dev
build-dev: ## Build development Docker image
	@echo "Building development Docker image..."
	@docker build -f DockerFile.dev -t $(DEV_IMAGE) .

.PHONY: run-dev
run-dev: build-dev ## Build and run development Docker container
	@echo "Running development container..."
	@docker run --rm -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		-v $(PWD):/app \
		$(DEV_IMAGE)
	@echo "Development server running at http://localhost:$(PORT)"

.PHONY: run-dev-attached
run-dev-attached: build-dev ## Build and run development Docker container (attached)
	@echo "Running development container (attached)..."
	@docker run --rm -it \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		-v $(PWD):/app \
		$(DEV_IMAGE)

# Utility targets
.PHONY: stop
stop: ## Stop running container
	@echo "Stopping container..."
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true

.PHONY: logs
logs: ## Show container logs
	@docker logs -f $(CONTAINER_NAME)

.PHONY: shell
shell: ## Access container shell
	@docker exec -it $(CONTAINER_NAME) /bin/bash

# Export requirements for Docker
.PHONY: export-requirements
export-requirements: ## Export poetry dependencies to requirements.txt
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Requirements exported to requirements.txt"