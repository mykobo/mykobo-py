release:
	semantic-release version --changelog

test:
	@source .venv/bin/activate && poetry run pytest