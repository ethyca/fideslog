.DEFAULT_GOAL := build-local

####################
# CONSTANTS
####################

REGISTRY := ethyca
IMAGE_TAG := $(shell git fetch --force --tags && git describe --tags --dirty --always)

IMAGE_NAME := fideslog
IMAGE := $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
IMAGE_LOCAL := $(REGISTRY)/$(IMAGE_NAME):local
IMAGE_LATEST := $(REGISTRY)/$(IMAGE_NAME):latest

# Disable TTY to perserve output within Github Actions logs
# CI env variable is always set to true in Github Actions
ifeq "$(CI)" "true"
    CI_ARGS:=--no-TTY
endif

# Run in Compose
RUN_NO_DEPS = docker compose run --no-deps --rm $(CI_ARGS) $(IMAGE_NAME)

####################
# Docker
####################

build:
	docker build --tag $(IMAGE) .

build-local:
	docker build --tag $(IMAGE_LOCAL) .

rebuild-local:
	docker build --no-cache --tag $(IMAGE_LOCAL) .

push: build
	docker tag $(IMAGE) $(IMAGE_LATEST)
	docker push $(IMAGE)
	docker push $(IMAGE_LATEST)

####################
# Dev
####################

.PHONY: api
api: build-local
	@echo "Spinning up the webserver..."
	@docker compose up $(IMAGE_NAME)
	@make teardown

lint:
	@echo "Running all static checks..."
	@$(RUN_NO_DEPS) black --exclude="sdk/python/_version\.py" fideslog/ tests/
	@$(RUN_NO_DEPS) isort fideslog/ tests/
	@$(RUN_NO_DEPS) mypy
	@$(RUN_NO_DEPS) pylint fideslog/
	@$(RUN_NO_DEPS) xenon fideslog --max-absolute B --max-modules B --max-average A --ignore "tests" --exclude "fideslog/sdk/python/_version.py"
	@echo "Completed all static checks!"

####################
# CI
####################

check-all: build-local isort black pylint mypy xenon pytest
	@echo "Running formatter, linter, typechecker and tests..."

black:
	@$(RUN_NO_DEPS) black --check --exclude="sdk/python/_version\.py" fideslog/ tests/

isort:
	$(RUN_NO_DEPS) isort --check fideslog/ tests/

mypy:
	@$(RUN_NO_DEPS) mypy

pylint:
	@$(RUN_NO_DEPS) pylint fideslog/

pytest:
	@docker compose up -d $(IMAGE_NAME)
	@$(RUN_NO_DEPS) pytest

xenon:
	@$(RUN_NO_DEPS) \
	xenon fideslog \
	--max-absolute B \
	--max-modules B \
	--max-average A \
	--ignore "tests" \
	--exclude "fideslog/sdk/python/_version.py"

####################
# Utils
####################

.PHONY: clean
clean:
	@echo "Cleaning project temporary files and installed dependencies..."
	@docker system prune -a --volumes
	@echo "Clean complete!"

.PHONY: teardown
teardown:
	@echo "Tearing down the dev environment..."
	@docker compose down
	@echo "Teardown complete"
