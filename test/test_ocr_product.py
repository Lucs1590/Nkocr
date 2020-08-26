import unittest
from PIL import Image

from src.ocr_product import OcrProduct
from pytest_socket import disable_socket, enable_socket


class TestProduct(unittest.TestCase):

    def test_path_processing(self):
        text = OcrProduct('test/ocr.png')
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing(self):
        enable_socket()
        text = OcrProduct(
            'https://project-elements-nk.s3.amazonaws.com/ocr.png')
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing_error(self):
        disable_socket()
        with self.assertRaises(ConnectionError):
            OcrProduct('https://project-elements-nk.s3.amazonaws.com/ocr.png')

    def test_image_processing(self):
        image = Image.open('test/ocr.png')
        text = OcrProduct(image)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_execution_time(self):
        text_and_time = OcrProduct('test/ocr.png', show_performace=True)
        has_time = text_and_time.execution_time and \
            text_and_time.show_performace and \
            len(eval(repr(text_and_time))) > 1
        self.assertTrue(has_time)

    def test_wrong_parameter_type(self):
        image = Image.open('test/ocr.png')
        with self.assertRaises(TypeError):
            OcrProduct(image, True)
