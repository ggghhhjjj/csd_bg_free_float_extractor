"""
Tests for the PDF processor functionality.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import logging

from csd_bg_free_float_extractor.extractor.processor import PDFProcessor, LogHandler


class TestLogHandler(unittest.TestCase):
    """Test the log handler functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)

        # Create a log handler
        self.log_handler = LogHandler(self.logger, self.output_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_setup_file_logger(self):
        """Test setting up a file logger."""
        file_handler = self.log_handler.setup_file_logger("test_file")
        self.assertIsNotNone(file_handler)
        self.assertFalse(self.log_handler.errors_logged)

        # The log file should not exist yet since delay=True
        log_file = self.output_dir / "test_file.errors.log"
        self.assertFalse(log_file.exists())

    def test_mark_error(self):
        """Test marking an error."""
        self.log_handler.setup_file_logger("test_file")
        self.assertFalse(self.log_handler.errors_logged)

        # Mark an error
        self.log_handler.mark_error()
        self.assertTrue(self.log_handler.errors_logged)

    def test_cleanup_no_errors(self):
        """Test cleanup when no errors occurred."""
        file_handler = self.log_handler.setup_file_logger("test_file")

        # Force file creation by writing a log message
        self.logger.warning("This is a test warning")
        log_file = self.output_dir / "test_file.errors.log"

        # Clean up with no errors marked
        self.log_handler.cleanup()

        # File should not exist (should be deleted)
        self.assertFalse(log_file.exists())

    def test_cleanup_with_errors(self):
        """Test cleanup when errors occurred."""
        file_handler = self.log_handler.setup_file_logger("test_file")

        # Force file creation by writing a log message
        self.logger.warning("This is a test warning")
        log_file = self.output_dir / "test_file.errors.log"

        # Mark an error and clean up
        self.log_handler.mark_error()
        self.log_handler.cleanup()

        # File should still exist
        self.assertTrue(log_file.exists())


class TestPDFProcessor(unittest.TestCase):
    """Test the PDF processor functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # Create a logger
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.ERROR)  # Suppress warnings during tests

        # Create a processor
        self.processor = PDFProcessor(self.input_dir, self.output_dir, self.logger)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)

    def test_initialization(self):
        """Test processor initialization."""
        self.assertEqual(self.processor.input_dir, Path(self.input_dir))
        self.assertEqual(self.processor.output_dir, Path(self.output_dir))
        self.assertEqual(self.processor.logger, self.logger)

        # Output directory should exist
        self.assertTrue(Path(self.output_dir).exists())

    def test_process_directory_empty(self):
        """Test processing an empty directory."""
        output_files = self.processor.process_directory()
        self.assertEqual(len(output_files), 0)


if __name__ == "__main__":
    unittest.main()