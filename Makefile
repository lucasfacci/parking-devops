APP = parking-devops

test:
	@bandit -r . -x '/venv/','/tests/'
	@black .
	@flake8 . --exclude venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up