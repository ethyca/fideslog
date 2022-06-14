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

####################
# CI
####################

check-all: build-local isort black pylint mypy xenon pytest
	@echo "Running formatter, linter, typechecker and tests..."

black:
	@$(RUN_NO_DEPS) black --check --exclude="sdk/python/_version\.py" fideslog/

isort:
	@echo "Running isort checks..."
	@docker-compose run $(IMAGE_NAME) \
		isort fideslog tests --check-only

mypy:
	@$(RUN_NO_DEPS) mypy

pylint:
	@$(RUN_NO_DEPS) pylint --ignore-patterns="sdk/python/_version\.py" fideslog/

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
	--exclude "fideslog/sdk/python/event.py,fideslog/sdk/python/_version.py"

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
