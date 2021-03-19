from time import time
from io import BytesIO
import pytesseract

from PIL import Image

import auxiliary as aux


class OcrProduct:
    def __init__(self,
                 image,
                 language: str = 'por',
                 spell_corrector=False,
                 show_performace: bool = False):
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

    def define_global_vars(self, language, show_performace, spell_corrector):
        if isinstance(language, str) and isinstance(show_performace, bool) \
                and isinstance(spell_corrector, bool):
            self.lang = language
            self.show_performace = show_performace
            self.spell_corrector = spell_corrector
        else:
            raise TypeError(
                'language variable must be a string, show_perf. and spell_corrector bool!')

    def process_image(self, image, _type):
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

    def run_online_img_ocr(self, image_url):
        image = aux.get_image_from_url(image_url)
        phrase = pytesseract.image_to_string(
            Image.open(BytesIO(image.content)), lang=self.lang)
        return phrase

    def run_path_img_ocr(self, image):
        phrase = pytesseract.image_to_string(Image.open(image), lang=self.lang)
        return phrase

    def run_img_ocr(self, image):
        phrase = pytesseract.image_to_string(image, lang=self.lang)
        return phrase
