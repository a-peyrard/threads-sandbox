PYTHON_MODULES := threads
PYTHONPATH := .
PYTEST := @env PYTHONPATH=$(PYTHONPATH) PYTEST=1 py.test
PYLINT := @env PYTHONPATH=$(PYTHONPATH) pylint --disable=I0011 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PEP8 := @env PYTHONPATH=$(PYTHONPATH) pycodestyle --repeat --ignore=E202,E501,E402
PYTHON := @env PYTHONPATH=$(PYTHONPATH) python
PIP := pip

REQUIREMENTS := -r requirements.txt

default: check-coding-style

requirements:
		@if [ -d wheelhouse ]; then \
			$(PIP) install -q --no-index --find-links=wheelhouse $(REQUIREMENTS); \
		else \
			$(PIP) install -q $(REQUIREMENTS); \
		fi

check-coding-style: requirements
		$(PEP8) $(PYTHON_MODULES)
		$(PYLINT) -E $(PYTHON_MODULES)

pylint-full: check-coding-style
		$(PYLINT) $(PYTHON_MODULES)

test: check-coding-style
		$(PYTEST)

check:
		$(PYTEST)

run:
		$(PYTHON) $(PYTHON_MODULES)/main.py

.PHONY: default requirements check-coding-style pylint-full test check