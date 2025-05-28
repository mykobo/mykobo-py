release:
	semantic-release version --changelog

test:
	poetry run pytest