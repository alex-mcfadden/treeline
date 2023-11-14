# IC50 data parser
## Description
This script parses inhibition and IC50 data from [Herreros et al 2015](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0135139#sec023), combining their data into a single row of useful data for a given compound. The relevant tables (Tables 1 and 7) are included in this repo, in the `/data` directory. 

## Usage

### Requirements
- Python 3.6+
- OpenPyXL for reading XLSX files
- Pytest for running tests

All requirements are included in the `requirements.txt` file. To install them, run `pip install -r requirements.txt`.

### Running the script

To run the script, simply run `python compound_parser.py`. This will output a file called `output.csv` in the current directory.

### Running tests

To run the tests, run `pytest` in the root directory of the repo.

