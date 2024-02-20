export DOCKER_IMAGE_NAME=streamlit-dashboard

requirements:
	echo "Exporting Python project dependencies"
	poetry export -f requirements.txt --output requirements.txt --without-hashes

dashboard:
	poetry run streamlit run main.py --server.runOnSave true

build: requirements
	echo "Building Docker image for trade_to_ohlc"
	docker build -t ${DOCKER_IMAGE_NAME} .

run: build
	echo "Starting trade_to_ohlc service"
	docker run --env ./.env -p 80:80 ${DOCKER_IMAGE_NAME}

