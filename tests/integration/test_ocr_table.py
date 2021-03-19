import unittest
import ast
from PIL import Image

from pytest_socket import disable_socket, enable_socket
from src.ocr_table import OcrTable


class TestTableIntegration(unittest.TestCase):

    def setUp(self):
        self.image_path = 'tests/fixtures/ocr.png'

    def test_path_processing(self):
        enable_socket()
        text = OcrTable(self.image_path)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing(self):
        enable_socket()
        text = OcrTable(
            'https://project-elements-nk.s3.amazonaws.com/ocr.png')
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing_error(self):
        disable_socket()
        with self.assertRaises(ConnectionError):
            OcrTable('https://project-elements-nk.s3.amazonaws.com/ocr.png')

    def test_image_processing(self):
        enable_socket()
        image = Image.open(self.image_path)
        text = OcrTable(image)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_execution_time(self):
        enable_socket()
        text_and_time = OcrTable(self.image_path, show_performace=True)
        has_time = text_and_time.execution_time and \
            text_and_time.show_performace and \
            len(ast.literal_eval(repr(text_and_time))) > 1
        self.assertTrue(has_time)

    def test_spell_corrector_flag(self):
        enable_socket()
        result = OcrTable(self.image_path, spell_corrector=True)
        has_spell_corrector = result.spell_corrector and \
            len(ast.literal_eval(repr(result))) > 1
        self.assertTrue(has_spell_corrector)

    def test_wrong_parameter_type(self):
        image = Image.open(self.image_path)
        with self.assertRaises(TypeError):
            OcrTable(image, True)


if __name__ == '__main__':
    unittest.main()
