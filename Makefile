ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip

test:
	$(PYTHON) -m pytest tests/

default:
	@cat Makefile

env:
	python3 -m venv $(ENV)
	$(PYTHON) -m pip install --upgrade pip

update: env
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m pylint bin/ lib/ tests/

test_enrich:
	cat mock_transcripts.jsonl | $(PYTHON) -u bin/enrich_transcripts.py | $(PYTHON) bin/validate_schema.py

run:
	cat test_ids | $(PYTHON) bin/clean_ids.py

.PHONY: load
load:
	@echo "Initiating Cloud Data Warehouse Synchronizer Node..."
	cat data/enriched_transcripts.jsonl | $(PYTHON) bin/load_snowflake.py

DOCKER_IMAGE = csh4bjuva/ds5111-pipeline:latest
DOCKER_INPUT = test_ids

.PHONY: docker-check docker-build docker-smoke docker-short
.PHONY: docker-run docker-push docker-clean docker-deploy

docker-check:
	docker ps

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-smoke:
	cat $(DOCKER_INPUT) | docker run -i $(DOCKER_IMAGE) \
		sh -c "python bin/clean_ids.py"

docker-short:
	cat $(DOCKER_INPUT) | docker run -i --env-file .env $(DOCKER_IMAGE) bash -c "python bin/clean_ids.py | python bin/extract_transcripts_oop.py"

docker-run:
	cat $(DOCKER_INPUT) | docker run -i --env-file .env $(DOCKER_IMAGE)

docker-push:
	docker push $(DOCKER_IMAGE)

docker-clean:
	@containers=$$(docker ps -aq); \
	if [ -n "$$containers" ]; then docker rm -f $$containers; fi
	@if docker image inspect $(DOCKER_IMAGE) >/dev/null 2>&1; then \
		docker rmi $(DOCKER_IMAGE); \
	else \
		echo "Pipeline image is already absent."; \
	fi

docker-deploy: docker-clean
	cat $(DOCKER_INPUT) | docker run -i --env-file .env $(DOCKER_IMAGE)
