#!/bin/bash
set -e

# Build the test Docker image
echo "Building test Docker image..."
docker build -t csd-bg-free-float-extractor-test -f Dockerfile.test .

# Run the tests
echo "Running tests..."
docker run --rm csd-bg-free-float-extractor-test

echo "Tests completed successfully!"