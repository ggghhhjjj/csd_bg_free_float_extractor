"""
Command-line interface functions for Bulgarian PDF extractor.
"""

import argparse
import logging
import time

from watchdog.observers import Observer

from .extractor.processor import PDFProcessor
from .extractor.utils import setup_logger
from .watcher.handler import PdfFileHandler


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Extract data from Bulgarian PDF files.")
    parser.add_argument("--input", "-i", required=True, help="Input directory with PDF files")
    parser.add_argument("--output", "-o", required=True, help="Output directory for CSV files")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch for new PDF files")
    parser.add_argument("--process", "-p", action="store_true", help="Process existing PDF files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def run_watcher(processor):
    """
    Set up and run the file system watcher.

    Args:
        processor (PDFProcessor): Processor for PDF files
    """
    event_handler = PdfFileHandler(processor)
    observer = Observer()
    observer.schedule(event_handler, str(processor.input_dir), recursive=False)
    observer.start()

    processor.logger.info(f"Watching directory {processor.input_dir} for PDF changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    """Main command-line entry point."""
    args = parse_arguments()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger("csd_bg_free_float_extractor", log_level)

    # Create the processor
    processor = PDFProcessor(args.input, args.output, logger)

    # Process existing files if requested
    if args.process:
        processor.process_directory()

    # Watch for new files if requested
    if args.watch:
        run_watcher(processor)

    # If neither --watch nor --process specified, process existing by default
    if not args.process and not args.watch:
        processor.process_directory()

    return 0
