import unittest
from PIL import Image
from src.auxiliary import Auxiliary


aux = Auxiliary()


class TestAuxiliary(unittest.TestCase):

    def test_of_tests(self):
        self.assertTrue(True)

    def test_image_type(self):
        image = Image.open('test/ocr.png')
        input_type = aux.get_input_type(image)
        self.assertEqual(input_type, 3)

    def test_path_type(self):
        path = 'test/ocr.png'
        input_type = aux.get_input_type(path)
        self.assertEqual(input_type, 2)

    def test_url_type(self):
        url = 'https://img.icons8.com/all/500/general-ocr.png'
        input_type = aux.get_input_type(url)
        self.assertEqual(input_type, 1)

    def test_wrong_type(self):
        string = 'a'
        with self.assertRaises(TypeError):
            aux.get_input_type(string)

    def test_to_opencv_conversion(self):
        ...

    def test_remove_alpha_channel(self):
        ...

    def test_brightness_contrast_optmization(self):
        ...

    def test_run_k_means(self):
        ...

    def test_centroid_histogram(self):
        ...

    def test_sort_colors(self):
        ...

    def test_resize_image(self):
        ...

    def test_dpi_upgrade(self):
        ...

    def test_morphologic_filters(self):
        ...

    def test_binarize_image(self):
        ...
