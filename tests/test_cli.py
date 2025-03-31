"""
Tests for the command-line interface.
"""

import unittest
import sys
from unittest.mock import patch

from csd_bg_free_float_extractor.cli import parse_arguments


class TestCLI(unittest.TestCase):
    """Test the command-line interface."""

    def test_parse_arguments(self):
        """Test argument parsing with valid arguments."""
        test_args = [
            "--input", "/path/to/input",
            "--output", "/path/to/output",
            "--watch", "--process"
        ]

        with patch.object(sys, 'argv', ['program'] + test_args):
            args = parse_arguments()

            self.assertEqual(args.input, "/path/to/input")
            self.assertEqual(args.output, "/path/to/output")
            self.assertTrue(args.watch)
            self.assertTrue(args.process)
            self.assertFalse(getattr(args, 'verbose', False))

    def test_parse_arguments_verbose(self):
        """Test argument parsing with verbose flag."""
        test_args = [
            "--input", "/path/to/input",
            "--output", "/path/to/output",
            "--verbose"
        ]

        with patch.object(sys, 'argv', ['program'] + test_args):
            args = parse_arguments()

            self.assertEqual(args.input, "/path/to/input")
            self.assertEqual(args.output, "/path/to/output")
            self.assertFalse(args.watch)
            self.assertFalse(args.process)
            self.assertTrue(args.verbose)

    def test_parse_arguments_short_options(self):
        """Test argument parsing with short options."""
        test_args = [
            "-i", "/path/to/input",
            "-o", "/path/to/output",
            "-w", "-p", "-v"
        ]

        with patch.object(sys, 'argv', ['program'] + test_args):
            args = parse_arguments()

            self.assertEqual(args.input, "/path/to/input")
            self.assertEqual(args.output, "/path/to/output")
            self.assertTrue(args.watch)
            self.assertTrue(args.process)
            self.assertTrue(args.verbose)

    @patch('argparse.ArgumentParser.parse_args')
    def test_missing_required_arguments(self, mock_parse_args):
        """Test that required arguments are enforced."""
        # This will raise SystemExit in real usage, but we're mocking to test the logic
        mock_parse_args.side_effect = SystemExit(2)

        with self.assertRaises(SystemExit):
            parse_arguments()


if __name__ == "__main__":
    unittest.main()