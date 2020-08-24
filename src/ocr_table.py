import pytesseract
import numpy as np
import cv2

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
        if isinstance(language, str) and \
                isinstance(show_performace, bool):
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

    def run_online_img_ocr(self, image_url):
        response = self.aux.get_image_from_url(image_url)
        phrase = self.run_pipeline(Image.open(BytesIO(response.content)))

        return phrase

    def run_path_img_ocr(self, image):
        phrase = self.run_pipeline(Image.open(image))
        return phrase

    def run_img_ocr(self, image):
        phrase = self.run_pipeline(image)
        return phrase

    def run_pipeline(self, image):
        if not isinstance(image, np.ndarray):
            image = self.aux.to_opencv_type(image)
        image = self.aux.remove_alpha_channel(image)
        image = self.aux.brightness_contrast_optimization(image, 1, 0.5)
        colors = self.aux.run_kmeans(image, 2)
        image = self.remove_lines(image, colors)
        image = self.aux.image_resize(image, height=image.shape[0]*4)
        image = self.aux.open_close_filter(image, cv2.MORPH_CLOSE)
        image = self.aux.brightness_contrast_optimization(image, 1, 0.5)
        image = self.aux.unsharp_mask(image, (3, 3), 0.5, 1.5, 0)
        image = self.aux.dilate_image(image, 1)

        image = self.aux.binarize_image(image)
        image = self.aux.open_close_filter(image, cv2.MORPH_CLOSE, 1)

        sorted_results = self.aux.east_process(image)
        sorted_chars = ' '.join(
            map(lambda position_and_word: position_and_word[1], sorted_results))

        return sorted_chars

    def remove_lines(self, image, colors):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_value, bin_image = cv2.threshold(
            gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))

        detected_h_lines = cv2.morphologyEx(
            bin_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        detected_v_lines = cv2.morphologyEx(
            bin_image, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

        h_contours = cv2.findContours(
            detected_h_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        h_contours = h_contours[0] if len(h_contours) == 2 else h_contours[1]
        for contour in h_contours:
            cv2.drawContours(image, [contour], -1, colors[0][0], 2)

        v_contours = cv2.findContours(
            detected_v_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_contours = v_contours[0] if len(v_contours) == 2 else v_contours[1]
        for contour in v_contours:
            cv2.drawContours(image, [contour], -1, colors[0][0], 2)

        return image
