import requests
import pytesseract

from PIL import Image
from time import time
from io import BytesIO
from pathlib import Path

from src.auxiliary import Auxiliary

class OCRTable(object):
    def __init__(self, image, show_performace: bool):
        self.aux = Auxiliary()

        input_type = self.aux.get_input_type(image)
        self.text = self.process_image(image, input_type)


    def process_image(self, image, _type):
        if _type == 1:
            ...
        elif _type == 2:
            ...
        elif _type == 3:
            ...
        else:
            ...
        start_time = time()
        phrase = pytesseract.image_to_string(Image.open('./images/tabela.png'), lang='por')
        print(phrase)
        print("Execution Time:", time() - start_time)
        