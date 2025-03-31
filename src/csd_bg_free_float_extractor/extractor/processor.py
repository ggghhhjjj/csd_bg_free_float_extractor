"""
File processing logic for Bulgarian market data extraction.
"""

import logging
from pathlib import Path

from .parser import PDFParser


class LogHandler:
    """Handles setting up and managing file-specific logging."""

    def __init__(self, logger, output_dir):
        """
        Initialize the log handler.

        Args:
            logger (Logger): Logger instance
            output_dir (Path): Directory to save log files
        """
        self.logger = logger
        self.output_dir = Path(output_dir)
        self.file_handler = None
        self.error_log_path = None
        self.errors_logged = False

    def setup_file_logger(self, filename):
        """
        Set up a file logger for errors specific to a file.

        Args:
            filename (str): Base filename for the log

        Returns:
            logging.FileHandler: Configured file handler
        """
        # Create a memory handler first that will only write to disk if errors occur
        self.error_log_path = self.output_dir / f"{filename}.errors.log"

        # Using a custom handler that only creates the file when needed
        self.file_handler = logging.FileHandler(self.error_log_path, mode='w', delay=True)
        self.file_handler.setLevel(logging.WARNING)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(file_format)
        self.logger.addHandler(self.file_handler)

        # Reset error tracking
        self.errors_logged = False

        return self.file_handler

    def mark_error(self):
        """Mark that an error has been logged."""
        self.errors_logged = True

    def cleanup(self):
        """Clean up logging and remove empty log files."""
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()
            self.file_handler = None

            # Delete the error log file if no errors were logged
            if not self.errors_logged and self.error_log_path and self.error_log_path.exists():
                try:
                    self.error_log_path.unlink()
                    self.logger.info("No errors encountered - no error log file created")
                except Exception as e:
                    self.logger.info(f"Failed to remove empty error log: {str(e)}")


class PDFProcessor:
    """Processes PDF files and exports results."""

    def __init__(self, input_dir, output_dir, logger=None):
        """
        Initialize the processor.

        Args:
            input_dir (str or Path): Directory containing PDF files
            output_dir (str or Path): Directory for output files
            logger (Logger, optional): Logger instance
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.logger = logger or logging.getLogger(__name__)

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize parser
        self.parser = PDFParser(self.logger)

    def process_pdf_file(self, pdf_path):
        """
        Process a single PDF file and export the results.

        Args:
            pdf_path (str or Path): Path to the PDF file

        Returns:
            tuple: (success status, output CSV path or None)
        """
        pdf_path = Path(pdf_path)

        # Set up file-specific logging
        log_handler = LogHandler(self.logger, self.output_dir)
        file_handler = log_handler.setup_file_logger(pdf_path.stem)

        # Extract data with error tracking
        df, extracted_date, errors_occurred = self.parser.extract_data_from_pdf(
            pdf_path,
            error_callback=log_handler.mark_error
        )

        # Clean up logging
        log_handler.cleanup()

        if df.empty:
            self.logger.error(f"No data extracted from {pdf_path}")
            return False, None

        # Create output filenames based on extracted date
        csv_filename = self.output_dir / f"{extracted_date}.csv"
        excel_filename = self.output_dir / f"{extracted_date}.xlsx"

        # Save to CSV with UTF-8 encoding (with BOM for Excel compatibility)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

        # Also save to Excel for easier viewing
        df.to_excel(excel_filename, index=False)

        self.logger.info(f"Saved {len(df)} records to {csv_filename} and {excel_filename}")
        return True, csv_filename

    def process_directory(self):
        """
        Process all PDF files in the input directory.

        Returns:
            list: List of successfully processed output files
        """
        self.logger.info(f"Processing all PDFs in {self.input_dir}")

        pdf_files = list(self.input_dir.glob("*.pdf"))

        if not pdf_files:
            self.logger.warning(f"No PDF files found in {self.input_dir}")
            return []

        output_files = []
        for pdf_file in pdf_files:
            success, output_file = self.process_pdf_file(pdf_file)
            if success and output_file:
                output_files.append(output_file)

        return output_files