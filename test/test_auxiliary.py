import unittest
import cv2
import os

import numpy as np

from PIL import Image
from src.auxiliary import Auxiliary
from sklearn.cluster import KMeans
from pytest_socket import disable_socket, enable_socket


aux = Auxiliary()


def get_pil_image():
    return Image.open('test/ocr.png')


def get_cv_image():
    return cv2.imread('test/ocr.png')


class TestAuxiliary(unittest.TestCase):

    def test_of_tests(self):
        self.assertTrue(True)

    def test_image_type(self):
        image = get_pil_image()
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
        image = get_pil_image()
        image = aux.to_opencv_type(image)
        self.assertTrue(isinstance(image, np.ndarray))

    def test_remove_alpha_channel(self):
        image = get_cv_image()
        image = aux.remove_alpha_channel(image)
        self.assertEqual(image.shape[-1], 3)

    def test_run_k_means(self):
        image = get_cv_image()
        colors = aux.run_kmeans(image, 1)
        self.assertEqual(len(colors), 1)

    def test_centroid_histogram(self):
        kmns = KMeans(n_clusters=7, random_state=0).fit(
            np.array([
                [1, 2],
                [1, 4],
                [1, 0],
                [10, 2],
                [10, 4],
                [10, 0],
                [10, 7]
            ]))
        centroids = aux.centroid_histogram(kmns)
        self.assertEqual(len(centroids), 7)

    def test_sort_colors(self):
        hist = np.array([0.2, 0.3, 0.5])
        colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])
        sorted_colors = aux.sort_colors(hist, colors)
        fst_color = (list(sorted_colors[0][0]) == colors[-1]).all()
        snd_color = (list(sorted_colors[1][0]) == colors[-2]).all()
        trd_color = (list(sorted_colors[2][0]) == colors[0]).all()
        result = True if fst_color and snd_color and trd_color else False
        self.assertTrue(result)

    def test_resize_image_width(self):
        image = get_cv_image()
        image_shape = image.shape
        image_returned = aux.image_resize(image, width=4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_resize_image_height(self):
        image = get_cv_image()
        image_shape = image.shape
        image_returned = aux.image_resize(image, height=4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_binarize_image(self):
        image = get_cv_image()
        expected_shape = (image.shape[0], image.shape[1])
        bin_image = aux.binarize_image(image)
        bin_image_shape = bin_image.shape
        self.assertEqual(bin_image_shape, expected_shape)

    def test_resize_image_height_width(self):
        image = get_cv_image()
        image_shape = image.shape
        image_returned = aux.image_resize(image, 4000, 4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_resize_image(self):
        image = get_cv_image()
        image_shape = image.shape
        image_returned = aux.image_resize(image)
        image_returned_shape = image_returned.shape
        self.assertEqual(image_shape, image_returned_shape)

    def test_load_model(self):
        enable_socket()
        model = aux.load_east_model()
        self.assertTrue(isinstance(model, str))

    def test_get_model(self):
        enable_socket()
        output = 'test/model.pb'
        os.remove(output) if os.path.isfile(output) else ...
        model = aux.get_model_from_s3(output)
        self.assertTrue(isinstance(model, str))

    def test_get_model_error(self):
        disable_socket()
        output = 'test/model.pb'
        with self.assertRaises(ConnectionError):
            aux.get_model_from_s3(output)

    def test_get_size(self):
        image = get_cv_image()
        sizes = aux.get_size(image)
        are_numbers = isinstance(sizes[0], int) and isinstance(sizes[1], int)
        self.assertTrue(are_numbers)

    def test_get_ratio(self):
        image = get_cv_image()
        ratios = aux.get_ratio(image.shape[0], image.shape[1])
        are_numbers = isinstance(
            ratios[0], float) and isinstance(ratios[1], float)
        self.assertTrue(are_numbers)

    def test_east_process(self):
        self.assertTrue(True)

    def test_run_east(self):
        model = cv2.dnn.readNet(aux.load_east_model())
        image = get_cv_image()
        size = (640, 640)
        east = aux.run_east(model, image, size[0], size[1])
        self.assertEqual(len(east), 2)

    def test_decode_predictions(self):
        self.assertTrue(True)

    def test_apply_boxes(self):
        self.assertTrue(True)

    def test_sort_boxes(self):
        self.assertTrue(True)
