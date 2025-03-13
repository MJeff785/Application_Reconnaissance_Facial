#Importing the necessary libraries
import sys
import os
import logging
import cv2 
import random
import numpy as np
from matplotlib import pyplot as pit 



def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Program started")
    if sys.version_info < (3, 9) or sys.version_info >= (3, 10):
        sys.exit("Error: This project requires Python 3.9.")

if __name__ == "__main__":
    main()
