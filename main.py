import sys

if sys.version_info < (3, 9) or sys.version_info >= (3, 10):
    sys.exit("Error: This project requires Python 3.9.")