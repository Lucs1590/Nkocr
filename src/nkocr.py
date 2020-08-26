import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ocr_table import ocr_tableOcrTable
from auxiliary import Auxiliary
from ocr_product import OcrProduct

if OcrTable and Auxiliary and OcrProduct:
    pass
