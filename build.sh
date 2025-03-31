#!/bin/bash

# Build the Docker image
docker build -t csd-bg-free-float-extractor .

echo "Docker image built successfully!"
echo "You can run it with:"
echo "docker run -v \$(pwd)/input:/data/input -v \$(pwd)/output:/data/output csd-bg-free-float-extractor"
echo ""
echo "Or use docker-compose:"
echo "docker-compose up -d"