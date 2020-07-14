import requests
import pytesseract

from PIL import Image
from time import time
from io import BytesIO
from pathlib import Path

from src.auxiliary import Auxiliary


class ocr_table(object):
    def __init__(self, image, language: str = "por", show_performace: bool = False):
        self.define_global_vars(language, show_performace)
        started_time = time()

        input_type = self.aux.get_input_type(image)
        self.text = self.process_image(image, input_type)

        self.execution_time = time() - started_time

    def __repr__(self):
        return repr(self.text) if not self.show_performace else repr([self.text, self.show_performace])

    def define_global_vars(self, language, show_performace):
        self.aux = Auxiliary()
        if isinstance(language, str) and isinstance(show_performace, bool):
            self.lang = language
            self.show_performace = show_performace
        else:
            raise TypeError(
                "language variable must need be a string and show_perf. bool!")

    def process_image(self, image, _type):
        if _type == 1:
            return self.run_online_img_ocr(image)
        elif _type == 2:
            return self.run_path_img_ocr(image)
        elif _type == 3:
            return self.run_img_ocr(image)
        else:
            raise NotImplementedError(
                "Method to this specific processing isn't implemented yet!")

    def run_online_img_ocr(self, image):
        response = requests.get(image)
        image = Image.open(BytesIO(response.content))
        phrase = pytesseract.image_to_string(image, lang=self.lang)
        return phrase

    def run_path_img_ocr(self, image):
        phrase = pytesseract.image_to_string(Image.open(image), lang=self.lang)
        return phrase

    def run_img_ocr(self, image):
        phrase = pytesseract.image_to_string(image, lang=self.lang)
        return phrase
