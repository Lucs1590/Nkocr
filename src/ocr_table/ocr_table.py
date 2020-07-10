import requests
import pytesseract

from PIL import Image
from time import time
from io import BytesIO
from pathlib import Path

from src.auxiliary import Auxiliary

class ocr_table(object):
    def __init__(self, image, show_performace: bool = False):
        self.aux = Auxiliary()

        input_type = self.aux.get_input_type(image)
        self.text = self.process_image(image, input_type)

    def __repr__(self):
        return self.text

    def process_image(self, image, _type):
        if _type == 1:
            return self.run_online_img_ocr(image)
        elif _type == 2:
            return self.run_path_img_ocr(image)
        elif _type == 3:
            return self.run_img_ocr(image)
        else:
            raise NotImplementedError("Method to this specific processing isn't implemented yet!")

    def run_online_img_ocr(self, image):
        ...

    def run_path_img_ocr(self, image):
        ...

    def run_img_ocr(self, image):
        ...
