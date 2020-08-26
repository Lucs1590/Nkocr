import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import auxiliary
from ocr_table import OcrTable
from ocr_product import OcrProduct

if OcrTable and auxiliary and OcrProduct:
    pass
