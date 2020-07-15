import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ocr_table import ocr_table
from auxiliary import Auxiliary

if ocr_table and Auxiliary:
    pass
