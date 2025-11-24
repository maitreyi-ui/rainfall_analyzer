# Rainfall Data Analyzer
## Overview of the Project
The Rainfall Data Analyzer is a command-line interface (CLI) tool designed to process a sequence of daily rainfall measurements (in mm) and generate a comprehensive summary along with actionable farming guidance. This project helps farmers and agricultural planners quickly assess rainfall patterns, identify dry spells, and detect heavy rain events to make informed decisions about irrigation, sowing, and drainage.



 ## Features

Core Rainfall Analysis: Calculates total, average, minimum, and maximum rainfall.

Dry and Heavy Day Identification: Flags days that fall below a configurable dry threshold or above a heavy threshold.

Rainfall Classification: Categorizes the overall rainfall into levels like Deficit, Adequate, High, or Excessive based on the average daily rainfall relative to the heavy threshold.


Agricultural Insights: Generates context-specific farming guidance, including advice for dry spells, extreme downpours, and managing overall rainfall levels.


Flexible Data Input: Accepts data via command-line arguments (--data), from a file (--file, supporting CSV and text), or interactively prompts the user for input if no data is provided.

## Technologies/Tools Used
Language: Python 3.8+

Core Libraries: Standard library only (e.g., dataclasses, statistics, argparse, pathlib, csv)


## Architecture: 
Modular structure with distinct modules for analysis, CLI, and data loading.


## Steps to Install & Run the Project
Clone the Repository:


git clone <your_repository_url>
cd rainfall-data-analyzer
Ensure Python is Installed: Make sure you have Python 3.8 or newer installed on your system.

Run the Analyzer: The project is structured to be run directly using the main entry point rainfall_analyzer.py.

Interactive Input (Default):


python rainfall_analyzer.py
The tool will prompt you to enter readings (e.g., 0 5.5 12 32 1.5)
Command-Line Data:



python rainfall_analyzer.py --data 0 5.5 12.1 35.0 1.2 0.0 15.8
File Input (CSV/Text):

Assuming you have a file named 'readings.csv'
python rainfall_analyzer.py --file readings.csv
Custom Thresholds:


python rainfall_analyzer.py --data 0 5.5 12 32 --dry-threshold 1.0 --heavy-threshold 25.0

## Instructions for Testing
Since this project primarily uses core Python features and standard libraries, the testing would involve validating the logic of the core functions, primarily in analysis.py.

Setup: Install a testing framework like pytest.


pip install pytest
Run Tests (Conceptual): Execute the test suite.

## screenshots
![WhatsApp Image 2025-11-24 at 18 10 46_9fa16066](https://github.com/user-attachments/assets/640e6552-8d8f-4417-b05e-47393787bafa)
