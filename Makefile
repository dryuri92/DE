#Build instructions for test task DE
GITCOMMIT?=$(shell git rev-parse --short HEAD)
IMAGE_TAG ?= $(GITCOMMIT)
IMAGE_NAME ?= backend-test-app
PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements.txt

run-locally:install
	$(PYTHON) main.py

build-docker:
	docker build . -t $(IMAGE_NAME):$(IMAGE_TAG)

compose-postgres:
	docker-compose -f ./compose/docker-compose.yaml up -d

compose-pandas:
	docker-compose -f ./compose/docker-compose-pandas.yaml up -d

run-tests:compose-postgres
	pytest

publish: build-docker
	docker push $(IMAGE_NAME):$(IMAGE_TAG)


