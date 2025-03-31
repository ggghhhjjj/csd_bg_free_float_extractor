"""
Constants and regex patterns for Bulgarian PDF extractor.
"""

import re

# Regex patterns
PATTERN_ROW = re.compile(r'^(?P<company>.+?)\s+(?P<emission_code>BG\S+)\s+'
                          r'(?P<total_shares>\d+)\s+(?P<free_float>\d+)\s+(?P<shareholders>\d+)$')

PATTERN_DATE = re.compile(r'към дата:\s*(\d{2}-\d{2}-\d{4})')
PATTERN_EMITENT_COUNT = re.compile(r'(\d+)\s+Брой\s+емитенти')

# Header text indicator
HEADER_TEXT = "Фрий флoут на публичните дружества регистрирани в Централен Депозитар към дата:"

# CSV column names
CSV_COLUMNS = ["Company", "Emission Code", "Total Shares", "Free Float", "Shareholders"]