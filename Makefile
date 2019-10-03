.PHONY: help clean test format run

.DEFAULT: help

help:
	@echo "make clean"
	@echo "       prepare development environment, use only once"
	@echo "make format"
	@echo "		  format code"
	@echo "make lint"
	@echo "       run lint"
	@echo "make test"
	@echo "       run tests"
	@echo "make run"
	@echo "       run the web application"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pyc|.DS_Store$$" | xargs rm -rf

format:
	black . --exclude venv

test: 
	pytest --verbose --color=yes

run: 
	python run.py
