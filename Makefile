APP = parking-devops

test:
	@flake8 . --exclude venv # --max-line-length=90
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up