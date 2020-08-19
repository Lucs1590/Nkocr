import unittest
from PIL import Image

from src.ocr_table import ocr_table
from pytest_socket import disable_socket, enable_socket


class TestTable(unittest.TestCase):

    def test_of_tests(self):
        self.assertTrue(True)

    def test_path_processing(self):
        text = ocr_table('test/ocr.png')
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing(self):
        enable_socket()
        text = ocr_table('https://img.icons8.com/all/500/general-ocr.png')
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_url_processing_error(self):
        disable_socket()
        with self.assertRaises(ConnectionError):
            ocr_table('https://img.icons8.com/all/500/general-ocr.png')

    def test_image_processing(self):
        image = Image.open('test/ocr.png')
        text = ocr_table(image)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_execution_time(self):
        text_and_time = ocr_table('test/ocr.png', show_performace=True)
        has_time = text_and_time.execution_time and \
            text_and_time.show_performace and \
            len(eval(repr(text_and_time))) > 1
        self.assertTrue(has_time)

    def test_wrong_type(self):
        image = Image.open('test/ocr.png')
        with self.assertRaises(TypeError):
            ocr_table(image, True)
