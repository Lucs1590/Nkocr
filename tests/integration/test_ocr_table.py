import unittest
import ast
from PIL import Image

from pytest_socket import disable_socket, enable_socket
from src.ocr_table import OcrTable


image_path = 'tests/ocr.png'


class TestTable(unittest.TestCase):

    def test_path_processing(self):
        text = OcrTable(image_path)
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
        image = Image.open(image_path)
        text = OcrTable(image)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_execution_time(self):
        text_and_time = OcrTable(image_path, show_performace=True)
        has_time = text_and_time.execution_time and \
            text_and_time.show_performace and \
            len(ast.literal_eval(repr(text_and_time))) > 1
        self.assertTrue(has_time)

    def test_wrong_parameter_type(self):
        image = Image.open(image_path)
        with self.assertRaises(TypeError):
            OcrTable(image, True)
