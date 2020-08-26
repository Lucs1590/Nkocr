import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from OcrTable import ocr_table
from auxiliary import Auxiliary
from ocr_product import ocr_product

if OcrTable and Auxiliary and ocr_product:
    pass
