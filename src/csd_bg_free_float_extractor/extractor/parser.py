"""
PDF parsing functions for Bulgarian market data.
"""

import logging
from pathlib import Path
from datetime import datetime

import pdfplumber
import pandas as pd

from ..constants import (
    PATTERN_ROW,
    PATTERN_DATE,
    PATTERN_EMITENT_COUNT,
    HEADER_TEXT,
    CSV_COLUMNS
)


def extract_date_from_text(text):
    """
    Extract the date from the PDF text.

    Args:
        text (str): Text content from PDF

    Returns:
        str: Extracted date in DD-MM-YYYY format or None if not found
    """
    if not text:
        return None

    match = PATTERN_DATE.search(text)
    if match:
        return match.group(1)  # Return the matched date
    return None


def parse_row(row_data, logger=None):
    """
    Parse a single row from the PDF.

    Args:
        row_data (str): The row data as a string.
        logger (Logger, optional): Logger for warnings.

    Returns:
        dict: Parsed row data if valid, None otherwise.
    """
    if not row_data or not isinstance(row_data, str):
        return None

    # Handle multi-line company names: Join all parts, preserving the order
    if "\n" in row_data:
        # Split the row into lines
        lines = row_data.strip().split("\n")

        # Assume BG code is in the first line
        # Find the position of "BG" in the first line
        bg_pos = lines[0].find("BG")

        if bg_pos > 0:
            # Extract company name part from first line (before BG)
            first_part = lines[0][:bg_pos].strip()
            # Extract rest of the first line (including BG code and numbers)
            rest_of_first_line = lines[0][bg_pos:].strip()
            # Combine with remaining lines
            remaining_lines = " ".join(lines[1:]).strip()
            # Reconstruct the row with company name properly assembled
            row_data = first_part + " " + remaining_lines + " " + rest_of_first_line
        else:
            # If BG isn't found in first line, just join everything with spaces
            row_data = " ".join(lines)

    # Apply regex matching
    match = PATTERN_ROW.match(row_data)

    if match:
        parsed_data = match.groupdict()
        return {
            "Company": parsed_data["company"].strip(),
            "Emission Code": parsed_data["emission_code"].strip(),
            "Total Shares": int(parsed_data["total_shares"]),
            "Free Float": int(parsed_data["free_float"]),
            "Shareholders": int(parsed_data["shareholders"])
        }
    else:
        if logger:
            logger.warning(f"Skipping row due to unexpected format: {row_data}")
        return None  # Invalid row


class PDFParser:
    """PDF parser for Bulgarian stock market data."""

    def __init__(self, logger=None):
        """
        Initialize the parser.

        Args:
            logger (Logger, optional): Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

    def extract_data_from_pdf(self, pdf_path, error_callback=None):
        """
        Extract structured tabular data from the Bulgarian stock market PDF.

        Args:
            pdf_path (Path): Path to the PDF file
            error_callback (callable, optional): Function to call on parsing errors

        Returns:
            tuple: (DataFrame of extracted data, extracted date string, errors occurred boolean)
        """
        self.logger.info(f"Processing PDF: {pdf_path}")

        # Lists to store extracted data
        extracted_data = []
        extracted_date = None
        emitent_count = None
        errors_occurred = False

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # First pass: find the date
                for page in pdf.pages:
                    text = page.extract_text()

                    if HEADER_TEXT in text:
                        extracted_date = extract_date_from_text(text)
                        if extracted_date:
                            self.logger.info(f"Extracted date: {extracted_date}")
                            break

                # If no date found, use the current date
                if not extracted_date:
                    extracted_date = datetime.now().strftime("%d-%m-%Y")
                    self.logger.warning(f"No date found in PDF. Using current date: {extracted_date}")
                    errors_occurred = True

                # Second pass: extract tabular data
                for page_num, page in enumerate(pdf.pages, 1):
                    # Try to extract as table first
                    table = page.extract_table()

                    if table:
                        for i, row in enumerate(table):
                            if row is None or len(row) == 0:
                                continue

                            # Skip the header row if detected
                            if i == 0 and any(h in (row[0] or '') for h in ["Емитент", "Емисия"]):
                                continue

                            # Check if this is the footer row with emitent count
                            row_text = " ".join(filter(None, row)).strip()
                            count_match = PATTERN_EMITENT_COUNT.search(row_text)
                            if count_match:
                                emitent_count = int(count_match.group(1))
                                self.logger.info(f"Found emitent count: {emitent_count}")
                                continue

                            # Join row contents if split across multiple cells
                            row_data = " ".join(filter(None, row)).strip()

                            # Parse row
                            parsed_row = parse_row(row_data, self.logger)

                            if parsed_row:
                                extracted_data.append(parsed_row)
                            else:
                                self.logger.warning(f"Failed to parse ${pdf_path} row on page {page_num}: {row_data}")
                                errors_occurred = True
                                if error_callback:
                                    error_callback()
                    else:
                        # If table extraction failed, try with raw text
                        self.logger.warning(f"No table found on page {page_num}, trying with raw text")
                        errors_occurred = True
                        if error_callback:
                            error_callback()

                        text = page.extract_text()
                        if text:
                            lines = text.split('\n')

                            for line in lines:
                                # Skip header lines
                                if any(h in line for h in ["Емитент", "Емисия", "Фрий флoут", "към дата"]):
                                    continue

                                # Check if this is the footer line with emitent count
                                count_match = PATTERN_EMITENT_COUNT.search(line)
                                if count_match:
                                    emitent_count = int(count_match.group(1))
                                    self.logger.info(f"Found emitent count: {emitent_count}")
                                    continue

                                # Try to parse as a data row
                                parsed_row = parse_row(line, self.logger)

                                if parsed_row:
                                    extracted_data.append(parsed_row)

            # Create DataFrame
            df = pd.DataFrame(extracted_data, columns=CSV_COLUMNS)

            # Validate extraction
            if not df.empty:
                if emitent_count and len(df) != emitent_count:
                    self.logger.warning(
                        f"Extracted {len(df)} rows but PDF indicates {emitent_count} emitents. "
                        f"Some data may be missing."
                    )
                    errors_occurred = True
                    if error_callback:
                        error_callback()
            else:
                self.logger.error("No data extracted from the PDF. Please check the format.")
                errors_occurred = True
                if error_callback:
                    error_callback()

            return df, extracted_date, errors_occurred

        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            errors_occurred = True
            if error_callback:
                error_callback()
            return pd.DataFrame(), extracted_date, errors_occurred