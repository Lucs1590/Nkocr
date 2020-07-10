import requests
import pytesseract

from PIL import Image
from time import time
from io import BytesIO
from pathlib import Path

from src.auxiliary import Auxiliary

class OCRTable(object):
    def __init__(self, image, show_performace: bool):
        ...

    def process_image(self, image, _type):
        ...
