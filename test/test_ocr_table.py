import unittest
from src.ocr_table import ocr_table


class TestTable(unittest.TestCase):
    
    def test_of_tests(self):
        self.assertTrue(True)

    def test_path_processing(self):
        text = ocr_table("test/ocr.png",False)
        type_output = isinstance(text,str)
        self.assertTrue(type_output)

    def test_url_processing(self):
        text = ocr_table("https://img.icons8.com/all/500/general-ocr.png")
        type_output = isinstance(text.text, str)
        self.assertTrue(type_output)

    def test_image_processing(self):
        ...