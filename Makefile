APP = parking-devops

test:
	@flake8 . --exclude venv # --max-line-length=90

compose:
	@docker compose build
	@docker compose up