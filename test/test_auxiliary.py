import unittest
import cv2

import numpy as np

from PIL import Image
from src.auxiliary import Auxiliary


aux = Auxiliary()


def get_PIL_image():
    return Image.open('test/ocr.png')


def get_CV_image():
    return cv2.imread('test/ocr.png')


class TestAuxiliary(unittest.TestCase):

    def test_of_tests(self):
        self.assertTrue(True)

    def test_image_type(self):
        image = get_PIL_image()
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
        image = get_PIL_image()
        image = aux.to_opencv_type(image)
        self.assertTrue(isinstance(image, np.ndarray))

    def test_remove_alpha_channel(self):
        image = get_CV_image()
        image = aux.remove_alpha_channel(image)
        self.assertEqual(image.shape[-1], 3)

    def test_brightness_contrast_optmization(self):
        ...

    def test_run_k_means(self):
        ...

    def test_centroid_histogram(self):
        ...

    def test_sort_colors(self):
        hist = np.array([0.2, 0.3, 0.5])
        colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
        sorted_colors = aux.sort_colors(hist, colors)
        fst_color = (list(sorted_colors[0][0]) == colors[-1]).all()
        snd_color = (list(sorted_colors[1][0]) == colors[-2]).all()
        trd_color = (list(sorted_colors[2][0]) == colors[0]).all()
        result = True if fst_color and snd_color and trd_color else False
        self.assertTrue(result)

    def test_resize_image(self):
        image = get_CV_image()
        image_shape = image.shape
        image_returned = aux.image_resize(image, 4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_dpi_upgrade(self):
        ...

    def test_morphologic_filters(self):
        ...

    def test_binarize_image(self):
        image = get_CV_image()
        expected_shape = (image.shape[0], image.shape[1])
        bin_image = aux.binarize_image(image)
        bin_image_shape = bin_image.shape
        self.assertEqual(bin_image_shape, expected_shape)
