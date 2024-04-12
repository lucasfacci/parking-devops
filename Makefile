APP = parking-devops

test:
	@black .
	@flake8 . --exclude venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up