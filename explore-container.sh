#!/bin/bash

echo "Exploring directory structure inside the container..."
docker run --rm \
  --user root \
  --entrypoint bash \
  csd-bg-free-float-extractor \
  -c "find /app -type d | sort"

echo -e "\nChecking Python path..."
docker run --rm \
  --user root \
  --entrypoint bash \
  csd-bg-free-float-extractor \
  -c "python -c 'import sys; print(sys.path)'"

echo -e "\nLooking for test files..."
docker run --rm \
  --user root \
  --entrypoint bash \
  csd-bg-free-float-extractor \
  -c "find /app -name 'test_*.py' | sort"