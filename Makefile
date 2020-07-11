shell:
	@pipenv shell

run:
	@uvicorn scheduler.backend.main:app --reload

lint:
	@pycodestyle --max-line-length=88 $(shell find . -name "*.py")

format:
	@black $(shell find . -name "*.py")
	@isort $(shell find . -name "*.py")
	@pycodestyle --max-line-length=88 $(shell find . -name "*.py")
