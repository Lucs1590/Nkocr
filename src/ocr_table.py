import requests
import pytesseract

from PIL import Image
from time import time
from io import BytesIO

from src.auxiliary import Auxiliary


class ocr_table(object):
    def __init__(self,
                 image,
                 language: str = 'por',
                 show_performace: bool = False):
        self.define_global_vars(language, show_performace)
        started_time = time()

        input_type = self.aux.get_input_type(image)
        self.text = self.process_image(image, input_type)

        self.execution_time = time() - started_time

    def __repr__(self):
        return repr(self.text) \
            if not self.show_performace \
            else repr([self.text, self.show_performace])

    def define_global_vars(self, language, show_performace):
        self.aux = Auxiliary()
        if isinstance(language, str) and isinstance(show_performace, bool):
            self.lang = language
            self.show_performace = show_performace
        else:
            raise TypeError(
                'language variable must need be a string and show_perf. bool!')

    def process_image(self, image, _type):
        if _type == 1:
            return self.run_online_img_ocr(image)
        elif _type == 2:
            return self.run_path_img_ocr(image)
        elif _type == 3:
            return self.run_img_ocr(image)
        else:
            raise NotImplementedError(
                'method to this specific processing isn'"'"'t implemented yet!')

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

    def run_pipeline(self, image):
        image = self.aux.to_opencv_type(image)
        image = self.aux.remove_alpha_channel(image)
        image = self.aux.brightness_contrast_optimization(image, 1, 0.5)
        colors = self.aux.to_kmeans(image, 2)
        image = self.remove_lines(image, colors)
        image = self.aux.image_resize(image, height=image.shape[0]*4)
        image = self.aux.open_close(image, cv2.MORPH_CLOSE)
        image = self.aux.brightness_contrast_optimization(image, 1, 0.5)
        image = self.aux.unsharp_mask(image, (3, 3), 0.5, 1.5, 0)
        image = self.aux.dilate(image, 1)

        image = self.aux.binarize_image(image)
        image = self.aux.open_close(image, cv2.MORPH_CLOSE, 1)

        return image
