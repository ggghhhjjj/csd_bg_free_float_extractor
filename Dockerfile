FROM python:3.10-slim

WORKDIR /app

# Copy all necessary files for installation
COPY setup.py pyproject.toml ./
COPY src/ ./src/

# Install the package in development mode to generate necessary egg-info files
RUN pip install --no-cache-dir -e .

# Compile the Python code to bytecode
RUN python -m compileall -b src/

# Create a proper package structure for installation
RUN mkdir -p /app/build/lib/csd_bg_free_float_extractor
RUN cp -r src/csd_bg_free_float_extractor/* /app/build/lib/csd_bg_free_float_extractor/

# Remove the source .py files from the build directory, keeping only the .pyc files
RUN find /app/build -name "*.py" -delete

# Install the package from the built directory
RUN pip install --no-cache-dir .

# Verify the installation
RUN python -c "import csd_bg_free_float_extractor; print(f'Package installed successfully: {csd_bg_free_float_extractor.__file__}')"

# Create directories for input and output
RUN mkdir -p /data/input /data/output

# Create a non-root user to run the application
RUN useradd -m -u 1026 -g users appuser
RUN chown -R appuser:users /data
USER appuser

# Set the command to run the extractor
ENTRYPOINT ["free-float-extractor", "--input", "/data/input", "--output", "/data/output"]

# Default to both processing existing files and watching for new ones
CMD ["--process", "--watch"]