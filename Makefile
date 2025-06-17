SHELL := /bin/bash
POETRY_CLI := $(shell which poetry)

# https://www.gnu.org/software/make/manual/make.html#Call-Function
confirm := read -r -p "⚠  Are you sure? [y/N] " response && [[ "$$response" =~ ^([yY][eE][sS]|[yY])$$ ]]

help: ## Print help for each target
	$(info Available commands:)
	$(info ==========================================================================================)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'


poetry-check: ## Checks if poetry is installed
ifeq ($(strip $(POETRY_CLI)),)
	@echo "ERROR: Please install poetry first!"
	exit 1
else
	@echo "Poetry is installed at: $(POETRY_CLI)"
endif

copy-env: ## Copies .env to .env.bak and creates a new one from .env.example
	@echo "Your may lose .env.bak"
	@if $(call confirm); then \
		cp .env .env.bak || true ; \
		cp .env.example .env ; \
	fi

# poetry hits keyring for most operations which adds unnecessary (for us) dependency on keyring:
# https://github.com/python-poetry/poetry/issues/1917#issuecomment-1235998997
setup-no-dev-dependencies: ## Installs dependencies without dev dependencies
	poetry env use python3.12
	PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring poetry install --without=dev

setup-dev-dependencies: ## Installs dev dependencies
	poetry env use python3.12
	PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring poetry install --only=dev

setup-dependencies: ## Uses python3.12 for .venv and installs dependencies
	poetry env use python3.12
	PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring poetry install

setup-pre-commit: ## Installs pre-commit-hook
	@echo "Installing pre-commit-hook"
	poetry run pre-commit install

setup-basic: poetry-check setup-no-dev-dependencies ## Sets up basic environment
	if [ ! -f .env ]; then cp .env.example .env; fi

setup: setup-basic setup-dev-dependencies setup-pre-commit ## Sets up local-development environment

run: ## Runs the service locally using poetry
	RUNTIME_ENVIRONMENT=local poetry run python -m debugpy --listen 0.0.0.0:8001 main.py

start: ## Starts the service using docker
	docker stop youtube-qna || true
	docker rm youtube-qna || true
	docker build -f DockerFile.dev -t youtube-qna .
	docker run -d \
	-v $(HOME)/.config/gcloud:/root/.config/gcloud \
	-v ./src:/usr/src/app/src \
	-v ./tests:/usr/src/app/tests \
	-v ./.env:/usr/src/app/.env \
	-v ./main.py:/usr/src/app/main.py \
	-p 7788:7788 --name youtube-qna \
	--user $(id -u):$(id -g) youtube-qna

clean: ## Cleans up the local-development environment except .env
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -f .coverage
	find . -name __pycache__ -type d -prune -exec rm -rf {} \;

merge-poetry-lock: ## Merges conflicted poetry.lock
	git diff --quiet pyproject.toml	# Ensure no unstaged change in pyproject.toml
	git checkout HEAD -- poetry.lock
	poetry lock --no-update
	git add poetry.lock

check-poetry-lock: ## Checks if poetry.lock corresponds to pyproject.toml and has correct content-hash
	@echo "Checking if poetry.lock corresponds to pyproject.toml and has correct content-hash"
	poetry check --lock
