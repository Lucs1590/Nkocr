import unittest
from src.ocr_table import ocr_table
from PIL import Image

class TestTable(unittest.TestCase):
    
    def test_of_tests(self):
        self.assertTrue(True)

    def test_path_processing(self):
        text = ocr_table("test/ocr.png")
        type_output = isinstance(text.text,str)
        self.assertTrue(type_output)

    def test_url_processing(self):
        text = ocr_table("https://img.icons8.com/all/500/general-ocr.png")
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_image_processing(self):
        image = Image.open("test/ocr.png")
        text = ocr_table(image)
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)
