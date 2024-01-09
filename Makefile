# Generate requirements.txt files for each service
requirements:
	cd trade_producer && make requirements
	cd trade_to_ohlc && make requirements
	cd ohlc_to_feature_store && make requirements

# Build Docker images for each service
build: requirements
	echo "Building Docker images"
	docker-compose build

# Start all services locally
start:
	echo "Starting local Kafka cluster"
	docker-compose up -d

# Stop all services locally
stop:
	echo "Stopping local Kafka cluster"
	docker-compose down


### Development

# lint_check:
# 	@echo "Checking for linting issues..."
# 	poetry run ruff check .

# lint:
# 	@echo "Fixing linting issues..."
# 	poetry run ruff check --fix .

format:
	@echo "Formatting code..."
	cd trade_producer && make format
	cd trade_to_ohlc && make format
	cd ohlc_to_feature_store && make format