.PHONY: build run run-process run-watch clean

# Create directories if they don't exist
init:
	mkdir -p input output

# Build the Docker image
build:
	docker build -t csd-bg-free-float-extractor .

# Run the container with both process and watch modes
run: init
	docker run -d --name free-float-extractor \
		-v $(PWD)/input:/data/input \
		-v $(PWD)/output:/data/output \
		csd-bg-free-float-extractor

# Run in process mode only (will exit after processing)
run-process: init
	docker run --rm \
		-v $(PWD)/input:/data/input \
		-v $(PWD)/output:/data/output \
		csd-bg-free-float-extractor --process

# Run in watch mode only (will keep running)
run-watch: init
	docker run -d --name free-float-extractor \
		-v $(PWD)/input:/data/input \
		-v $(PWD)/output:/data/output \
		csd-bg-free-float-extractor --watch

# Stop and remove the container
stop:
	docker stop free-float-extractor || true
	docker rm free-float-extractor || true

# Run using docker-compose
compose-up: init
	docker-compose up -d

# Stop the docker-compose services
compose-down:
	docker-compose down

# Clean up
clean: stop
	docker rmi csd-bg-free-float-extractor || true