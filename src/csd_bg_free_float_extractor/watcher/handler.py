"""
File system event handling for monitoring PDF files.
"""

import logging
from pathlib import Path

from watchdog.events import FileSystemEventHandler


class PdfFileHandler(FileSystemEventHandler):
    """Handler for PDF file system events."""

    def __init__(self, processor):
        """
        Initialize the handler.

        Args:
            processor (PDFProcessor): Processor instance for PDFs
        """
        super().__init__()
        self.processor = processor
        self.logger = processor.logger or logging.getLogger(__name__)

    def on_created(self, event):
        """
        Handle file creation events.

        Args:
            event (FileSystemEvent): The file system event
        """
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            self.logger.info(f"New PDF detected: {event.src_path}")
            self.processor.process_pdf_file(Path(event.src_path))

    def on_modified(self, event):
        """
        Handle file modification events.

        Args:
            event (FileSystemEvent): The file system event
        """
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            self.logger.info(f"Modified PDF detected: {event.src_path}")
            self.processor.process_pdf_file(Path(event.src_path))