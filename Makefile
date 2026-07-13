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
