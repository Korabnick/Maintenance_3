VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) main.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +

.PHONY: install test run clean
