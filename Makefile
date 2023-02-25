## Python dev
lint:
	poetry run black . --check
	poetry run flake8 --max-line-length 88

# todo: update flake8 to use the config file
format:
	poetry run pre-commit run --all-files
	poetry run black .
	poetry run flake8 --max-line-length 88
