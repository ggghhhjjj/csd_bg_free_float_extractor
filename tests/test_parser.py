"""
Tests for the PDF parser functionality.
"""

import unittest
import logging

from csd_bg_free_float_extractor.extractor.parser import parse_row, extract_date_from_text, PDFParser


class TestParseRow(unittest.TestCase):
    """Test the row parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.ERROR)  # Suppress warnings during tests

    def test_valid_row(self):
        """Test parsing a valid data row."""
        row = '235 ХОЛДИНГС АД BG1100017174 5109000 2583625 41'
        expected = {
            "Company": "235 ХОЛДИНГС АД",
            "Emission Code": "BG1100017174",
            "Total Shares": 5109000,
            "Free Float": 2583625,
            "Shareholders": 41
        }
        self.assertEqual(parse_row(row, self.logger), expected)

    def test_valid_multiline_row(self):
        """Test parsing a valid multiline data row."""
        row = 'БПД Индустриален Фонд за Недвижими BG1100008157 7900000 0 1\nИмоти"АДСИЦ'
        expected = {
            "Company": 'БПД Индустриален Фонд за Недвижими Имоти"АДСИЦ',
            "Emission Code": "BG1100008157",
            "Total Shares": 7900000,
            "Free Float": 0,
            "Shareholders": 1
        }
        self.assertEqual(parse_row(row, self.logger), expected)

    def test_invalid_row(self):
        """Test parsing an invalid row."""
        row = 'Invalid Data Here'
        self.assertIsNone(parse_row(row, self.logger))

    def test_empty_row(self):
        """Test parsing an empty row."""
        row = ''
        self.assertIsNone(parse_row(row, self.logger))

    def test_none_input(self):
        """Test parsing a None input."""
        row = None
        self.assertIsNone(parse_row(row, self.logger))


class TestExtractDate(unittest.TestCase):
    """Test the date extraction functionality."""

    def test_extract_valid_date(self):
        """Test extracting a valid date from text."""
        text = "Фрий флoут на публичните дружества регистрирани в Централен Депозитар към дата: 28-02-2025"
        self.assertEqual(extract_date_from_text(text), "28-02-2025")

    def test_extract_no_date(self):
        """Test extracting date from text without a date."""
        text = "Some random text without a date"
        self.assertIsNone(extract_date_from_text(text))

    def test_extract_date_empty_text(self):
        """Test extracting date from empty text."""
        text = ""
        self.assertIsNone(extract_date_from_text(text))

    def test_extract_date_none_text(self):
        """Test extracting date from None text."""
        text = None
        self.assertIsNone(extract_date_from_text(text))


class TestPDFParser(unittest.TestCase):
    """Test the PDF parser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.ERROR)  # Suppress warnings during tests
        self.parser = PDFParser(self.logger)

    def test_parser_initialization(self):
        """Test that the parser initializes correctly."""
        self.assertIsNotNone(self.parser)
        self.assertEqual(self.parser.logger, self.logger)


if __name__ == "__main__":
    unittest.main()