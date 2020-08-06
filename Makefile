shell:
	@pipenv shell

run:
	@uvicorn --host 0.0.0.0 scheduler.backend.main:app --reload --log-level debug

lint:
	@pycodestyle --max-line-length=88 $(shell find . -name "*.py")

format:
	@black $(shell find . -name "*.py")
	@isort $(shell find . -name "*.py")
	@pycodestyle --max-line-length=88 $(shell find . -name "*.py")
