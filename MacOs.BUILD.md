# Setting up Bulgarian Free Float Extractor on macOS M1 with Docker Desktop

These instructions will guide you through running the Bulgarian Free Float Extractor Docker container on your M1 Mac.

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3 chip)
- Docker Desktop for Mac installed and running
- Terminal access

## Option 1: Using Makefile (Recommended)

The included Makefile provides easy commands for building and running the container.

1. **Open Terminal** and navigate to the project directory.

2. **Build the Docker image**:
   ```
   make build
   ```

3. **Create necessary folders and run the container**:
   ```
   make run
   ```
   
   This command will:
   - Create input and output directories if they don't exist
   - Start the container in both process and watch modes

4. **Alternative run options**:
   - To process existing files only (container will exit after processing):
     ```
     make run-process
     ```
   - To watch for new files only (container will keep running):
     ```
     make run-watch
     ```

5. **Stopping the container**:
   ```
   make stop
   ```

6. **Cleaning up**:
   ```
   make clean
   ```

## Option 2: Using Docker Compose

1. **Open Terminal** and navigate to the project directory.

2. **Create the necessary directories**:
   ```bash
   mkdir -p input output
   ```

3. **Build and start the container**:
   ```bash
   docker-compose up -d
   ```

4. **Stop the container**:
   ```bash
   docker-compose down
   ```

## Option 3: Using Docker Commands Directly

1. **Build the image**:
   ```bash
   docker build -t csd-bg-free-float-extractor .
   ```

2. **Run the container** (both process and watch modes):
   ```bash
   docker run -d --name free-float-extractor \
     -v "$(pwd)/input:/data/input" \
     -v "$(pwd)/output:/data/output" \
     csd-bg-free-float-extractor
   ```

3. **View logs**:
   ```bash
   docker logs -f free-float-extractor
   ```

4. **Stop and remove the container**:
   ```bash
   docker stop free-float-extractor
   docker rm free-float-extractor
   ```

## Using the Application

1. **Place PDF files** in the `input` directory.

2. **Check results** in the `output` directory:
   - CSV files (UTF-8 with BOM for Excel compatibility)
   - Excel (.xlsx) files for easy viewing
   - Error logs (if any errors occurred during processing)

## Troubleshooting

- **Apple Silicon compatibility**: 
  The Docker image is based on Python 3.10-slim which has multi-architecture support including ARM64. No special flags are needed for M1 compatibility.

- **Performance issues**:
  - If you experience slower performance, check Docker Desktop resource allocation
  - Increase memory and CPU allocation in Docker Desktop preferences

- **File permission issues**:
  - The container runs as a non-root user for security
  - If experiencing permission problems, check the ownership of your input/output directories