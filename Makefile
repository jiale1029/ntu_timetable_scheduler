shell:
	@pipenv shell

run:
	@uvicorn scheduler.backend.main:app --reload
