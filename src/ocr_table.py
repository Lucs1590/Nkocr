from time import time
from io import BytesIO

import numpy as np
import cv2

from PIL import Image

import src.auxiliary as aux


class OcrTable:
    def __init__(self,
                 image,
                 language: str = 'eng',
                 spell_corrector: bool = False,
                 show_performace: bool = False):
        """ # OcrTable
        This class is responsible for the image processing and text extraction from nutritional facts tables.

        Args:
            image (str, np.ndarray, PIL.Image): image to be processed
            language (str, optional): language of the text to be extracted. Defaults to 'eng'.
            spell_corrector (bool, optional): if True, the text will be spell corrected. Defaults to False.
            show_performace (bool, optional): if True, the execution time will be shown. Defaults to False.

        Raises:
            TypeError: if language variable isn't a string, show_perf. and spell_corrector aren't bool
            NotImplementedError: if the method to process the image isn't implemented yet

        Returns:
            OcrTable: object with the text extracted from the image.
        """
        self.define_global_vars(language, show_performace, spell_corrector)
        started_time = time()

        input_type = aux.get_input_type(image)
        self.text = process_image(image, input_type)

        if self.spell_corrector:
            sym_spell = aux.load_dict_to_memory()
            self.text = [aux.get_word_suggestion(
                sym_spell, input_term) for input_term in self.text.split(' ')]
            self.text = ' '.join(self.text)

        self.execution_time = time() - started_time

    def __repr__(self):
        return repr(self.text) \
            if not self.show_performace \
            else repr([self.text, self.show_performace])

    def define_global_vars(self, language: str, show_performace: bool, spell_corrector: bool) -> None:
        """ # Define Global Variables
        This method defines the global variables of the class.

        Args:
            language (str): The language of the text to be extracted.
            show_performace (bool): If True, the execution time will be shown.
            spell_corrector (bool): If True, the text will be spell corrected.

        Raises:
            TypeError: if language variable isn't a string, show_perf. and spell_corrector aren't bool.
        """
        if isinstance(language, str) and \
                isinstance(show_performace, bool) and \
                isinstance(spell_corrector, bool):
            self.lang = language
            self.show_performace = show_performace
            self.spell_corrector = spell_corrector
        else:
            raise TypeError(
                'language variable must be a string, show_perf. and spell_corrector bool!')


def process_image(image, _type: int) -> str:
    """ # Process Image
    This method is responsible for processing the image and extracting the text from it.

    Args:
        image (str, np.ndarray, PIL.Image): image to be processed
        _type (int): type of the input image

    Raises:
        NotImplementedError: if the method to process the image isn't implemented yet.

    Returns:
        str: text extracted from the image.
    """
    if _type == 1:
        processed_img = run_online_img_ocr(image)
    elif _type == 2:
        processed_img = run_path_img_ocr(image)
    elif _type == 3:
        processed_img = run_img_ocr(image)
    else:
        raise NotImplementedError(
            'method to this specific processing isn'"'"'t implemented yet!')
    return processed_img


def run_online_img_ocr(image_url: str) -> str:
    """ # Run Online Image OCR
    This method is responsible for processing the image and extracting the text from it.

    Args:
        image_url (str): url of the image to be processed.

    Returns:
        str: text extracted from the image.
    """
    image = aux.get_image_from_url(image_url)
    phrase = run_pipeline(Image.open(BytesIO(image.content)))

    return phrase


def run_path_img_ocr(image: str) -> str:
    """ # Run Path Image OCR
    This method is responsible for processing the image and extracting the text from it.

    Args:
        image (str): path of the image to be processed.

    Returns:
        str: text extracted from the image.
    """
    phrase = run_pipeline(Image.open(image))
    return phrase


def run_img_ocr(image: np.ndarray) -> str:
    """ # Run Image OCR
    This method is responsible for processing the image and extracting the text from it.

    Args:
        image (np.ndarray): image to be processed.

    Returns:
        str: text extracted from the image.
    """
    phrase = run_pipeline(image)
    return phrase


def run_pipeline(image) -> str:
    """ # Run Pipeline
    This method is responsible for processing the image and extracting the text from it.

    Args:
        image (np.ndarray, PIL.Image): image to be processed.

    Returns:
        str: text extracted from the image.
    """
    if not isinstance(image, np.ndarray):
        image = aux.to_opencv_type(image)
    image = aux.remove_alpha_channel(image)
    image = aux.brightness_contrast_optimization(image, 1, 0.5)
    colors = aux.run_kmeans(image, 2)
    image = remove_lines(image, colors)
    image = aux.image_resize(image, height=image.shape[0]*4)
    image = aux.open_close_filter(image, cv2.MORPH_CLOSE)
    image = aux.brightness_contrast_optimization(image, 1, 0.5)
    image = aux.unsharp_mask(image, (3, 3), 0.5, 1.5, 0)
    image = aux.dilate_image(image, 1)

    image = aux.binarize_image(image)
    image = aux.open_close_filter(image, cv2.MORPH_CLOSE, 1)

    sorted_results = aux.east_process(image)
    sorted_chars = ' '.join(
        map(lambda position_and_word: position_and_word[1], sorted_results))

    return sorted_chars


def remove_lines(image: np.ndarray, colors: np.ndarray) -> np.ndarray:
    """ # Remove Lines
    This method is responsible for removing the lines from the image.

    Args:
        image (np.ndarray): image to be processed.
        colors (np.ndarray): colors of the image.

    Returns:
        np.ndarray: image without lines.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bin_image = cv2.threshold(
        gray_image,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    h_contours = get_contours(bin_image, (25, 1))
    v_contours = get_contours(bin_image, (1, 25))

    for contour in h_contours:
        cv2.drawContours(image, [contour], -1, colors[0][0], 2)

    for contour in v_contours:
        cv2.drawContours(image, [contour], -1, colors[0][0], 2)

    return image


def get_contours(bin_image: np.ndarray, initial_kernel: tuple) -> list:
    """ # Get Contours
    This method is responsible for getting the contours of the image lines.

    Args:
        bin_image (np.ndarray): image to be processed.
        initial_kernel (tuple): initial kernel to be used.

    Returns:
        list: contours of the image lines.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, initial_kernel)

    detected_lines = cv2.morphologyEx(
        bin_image, cv2.MORPH_OPEN, kernel, iterations=2)

    contours = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    return contours
