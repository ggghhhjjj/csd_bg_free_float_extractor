# Bulgarian PDF Data Extractor

This Python tool extracts tabular data from Bulgarian PDF files containing free float information of public companies registered in the Central Depository.

## Features

- Extracts company data from standardized Bulgarian PDF files
- Identifies and extracts the date from the introductory text
- Parses tabular data into structured format
- Exports the data to CSV files named after the extracted date
- Provides detailed error logging (only when errors occur)
- Watches for new or modified PDF files in the input directory
- Supports custom input and output directories

## Installation

### Production Installation

For users who just want to use the tool:

1. Clone this repository:
   ```bash
   git clone https://github.com/ggghhhjjj/csd_bg_free_float_extractor.git
   cd csd_bg_free_float_extractor
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install .
   ```

### Development Installation

For developers who want to contribute to the project:

1. Clone this repository:
   ```bash
   git clone https://github.com/ggghhhjjj/csd_bg_free_float_extractor.git
   cd csd_bg_free_float_extractor
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Basic Usage

Process existing PDF files in a directory:

```bash
free-float-extractor --input /path/to/pdf/files --output /path/to/output/directory
```

Alternatively, you can use the module directly:

```bash
python -m csd_bg_free_float_extractor --input /path/to/pdf/files --output /path/to/output/directory
```

### Watch for New Files

Watch a directory for new or modified PDF files:

```bash
free-float-extractor --input /path/to/pdf/files --output /path/to/output/directory --watch
```

### Process Files and Then Watch

Process existing files and then continue watching for new files:

```bash
free-float-extractor --input /path/to/pdf/files --output /path/to/output/directory --process --watch
```

### Enable Verbose Logging

For more detailed logging, use the verbose flag:

```bash
free-float-extractor --input /path/to/pdf/files --output /path/to/output/directory --verbose
```

## Output Files

For each processed PDF file, the following outputs are generated:

1. A CSV file named after the extracted date (e.g., `28-02-2025.csv`)
2. An Excel file with the same name (e.g., `28-02-2025.xlsx`)
3. An error log file (e.g., `28-02-2025.errors.log`) - **only created if errors occur**

The CSV and Excel files contain the following columns:
- Company
- Emission Code
- Total Shares
- Free Float
- Shareholders

## Docker Support

The project includes Docker support for easy deployment.

### Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Using Direct Docker Commands

```bash
# Build the image
docker build -t csd-bg-free-float-extractor .

# Run the container
docker run -d --name free-float-extractor \
  -v "$(pwd)/input:/data/input" \
  -v "$(pwd)/output:/data/output" \
  csd-bg-free-float-extractor
```

## Testing

Run all tests with:

```bash
python -m pytest tests/
```

Or run specific test modules:

```bash
python -m pytest tests/test_parser.py
python -m pytest tests/test_processor.py
python -m pytest tests/test_cli.py
```

### Running Tests with Docker

You can also run tests inside a Docker container:

```bash
./run-tests.sh
```

## Technical Details

The extractor uses several strategies to handle the Bulgarian PDF data:

1. **Table Extraction**: Attempts to extract tables directly using pdfplumber
2. **Text Parsing**: Falls back to text extraction and line-by-line parsing if table extraction fails
3. **Pattern Matching**: Uses regular expressions to identify and parse data rows
4. **Multi-line Handling**: Special handling for company names that span multiple lines

## Extending the Project

The modular design makes it easy to extend functionality:

- Add new parsing strategies in `extractor/parser.py`
- Add output formats in `extractor/processor.py`
- Enhance the watcher's behavior in `watcher/handler.py`

## Troubleshooting

- If you encounter issues with character encoding, check that your PDF files use a standard encoding.
- For PDFs that don't parse correctly, check the generated error log for details.
- If the date extraction fails, the current date will be used as a fallback.

## License

MIT License