#!/usr/bin/env python3
"""
Setup script for Bulgarian PDF Extractor.
"""

from setuptools import setup, find_packages

long_description = """
Bulgarian PDF Data Extractor

A tool for extracting tabular data from Bulgarian PDF files containing
free float information of public companies registered in the Central Depository.

Features:
- Extracts company data from standardized Bulgarian PDF files
- Identifies and extracts the date from the introductory text
- Parses tabular data into structured format
- Exports the data to CSV files named after the extracted date
- Provides detailed error logging (only when errors occur)
- Watches for new or modified PDF files in the input directory
- Supports custom input and output directories
"""

setup(
    name="csd_bg_free_float_extractor",
    version="0.1.0",
    author="George",
    author_email="no6ni4ka@gmail.com",
    description="Extract tabular data from Bulgarian PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/csd_bg_free_float_extractor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    # Runtime dependencies only
    install_requires=[
        "pdfplumber>=0.7.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "watchdog>=2.1.0",
    ],
    # Development dependencies
    extras_require={
        "dev": [
            "setuptools>=42",
            "wheel",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'free-float-extractor=csd_bg_free_float_extractor.cli:main',
        ],
    },
)
