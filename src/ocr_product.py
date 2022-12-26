from time import time
from io import BytesIO
import pytesseract

from PIL import Image

import src.auxiliary as aux


class OcrProduct:
    def __init__(self,
                 image,
                 language: str = 'eng',
                 spell_corrector=False,
                 show_performace: bool = False):
        """ # OcrProduct
        This class is responsible for the image processing and text extraction from product packaging images.

        Args:
            image (str, np.ndarray, PIL.Image): image to be processed.
            language (str, optional): language of the text to be extracted. Defaults to 'eng'.
            spell_corrector (bool, optional): if True, the text will be spell corrected. Defaults to False.
            show_performace (bool, optional): if True, the execution time will be shown. Defaults to False.

        Raises:
            TypeError: if language variable isn't a string, show_perf. and spell_corrector aren't bool.
            NotImplementedError: if the method to process the image isn't implemented yet.

        Returns:
            OcrProduct: object with the text extracted from the image.
        """
        self.define_global_vars(language, show_performace, spell_corrector)
        started_time = time()

        input_type = aux.get_input_type(image)
        self.text = self.process_image(image, input_type)

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
        if isinstance(language, str) and isinstance(show_performace, bool) \
                and isinstance(spell_corrector, bool):
            self.lang = language
            self.show_performace = show_performace
            self.spell_corrector = spell_corrector
        else:
            raise TypeError(
                'language variable must be a string, show_perf. and spell_corrector bool!')

    def process_image(self, image, _type: int) -> str:
        """ # Process Image
        This method is responsible for processing the image and extracting the text from it.

        Args:
            image (str, np.ndarray, PIL.Image): image to be processed.
            _type (int): type of the input image.

        Raises:
            NotImplementedError: if the method to process the image isn't implemented yet.

        Returns:
            str: text extracted from the image.
        """
        if _type == 1:
            processed_img = self.run_online_img_ocr(image)
        elif _type == 2:
            processed_img = self.run_path_img_ocr(image)
        elif _type == 3:
            processed_img = self.run_img_ocr(image)
        else:
            raise NotImplementedError(
                'method to this specific processing isn'"'"'t implemented yet!')
        return processed_img

    def run_online_img_ocr(self, image_url: str) -> str:
        """ # Run Online Image OCR
        This method is responsible for processing the image and extracting the text from it.

        Args:
            image_url (str): url of the image to be processed.

        Returns:
            str: text extracted from the image.
        """
        image = aux.get_image_from_url(image_url)
        phrase = pytesseract.image_to_string(
            Image.open(BytesIO(image.content)), lang=self.lang)
        return phrase

    def run_path_img_ocr(self, image: str) -> str:
        """ # Run Path Image OCR
        This method is responsible for processing the image and extracting the text from it.

        Args:
            image (str): path of the image to be processed.

        Returns:
            str: text extracted from the image.
        """
        phrase = pytesseract.image_to_string(Image.open(image), lang=self.lang)
        return phrase

    def run_img_ocr(self, image) -> str:
        """ # Run Image OCR
        This method is responsible for processing the image and extracting the text from it.

        Args:
            image (Image, np.ndarray): image to be processed.

        Returns:
            str: text extracted from the image.
        """
        phrase = pytesseract.image_to_string(image, lang=self.lang)
        return phrase
