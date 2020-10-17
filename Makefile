.PHONY: clean lint

PY = python

# Install dependencies with pip
requirements: clean
	$(PY) -m pip install -U pip setuptools wheel
	$(PY) -m pip install -r requirements.txt

# Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

# Lint using pycodestyle
lint:
	pycodestyle .

# Run tests
check: lint
	pytest .