# install Python Poetry and Python project dependencies
install:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install
	poetry run pip install hopsworks

requirements:
	echo "Exporting Python project dependencies"
	# poetry run pip freeze > requirements.txt
	poetry export -f requirements.txt --output requirements.txt --without-hashes

format:
	echo "Formatting Python code"
	poetry run ruff format .

lint_check:
	@echo "Checking for linting issues..."
	poetry run ruff check .

lint:
	@echo "Fixing linting issues..."
	poetry run ruff check --fix .