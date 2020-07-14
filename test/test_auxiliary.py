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
        self.assertEqual(input_type, 3)

    def test_path_type(self):
        path = "test/ocr.png"
        input_type = aux.get_input_type(path)
        self.assertEqual(input_type, 2)

    def test_url_type(self):
        url = "https://img.icons8.com/all/500/general-ocr.png"
        input_type = aux.get_input_type(url)
        self.assertEqual(input_type, 1)

    def test_wrong_type(self):
        string = "a"
        with self.assertRaises(TypeError) as error:
            aux.get_input_type(string)
