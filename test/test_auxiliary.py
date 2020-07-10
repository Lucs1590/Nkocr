import unittest
from PIL import Image
from src.auxiliary import Auxiliary


aux = Auxiliary()
class TestAuxiliary(unittest.TestCase):

    def test_of_tests(self):
        self.assertTrue(True)

    def test_image_type(self):
        image = Image.open("test/ocr.png")
        input_type = aux.get_input_type(image)
        self.assertEqual(input_type,3)
    
    def test_path_type(self):
        ...
    
    def test_url_type(self):
        ...
    