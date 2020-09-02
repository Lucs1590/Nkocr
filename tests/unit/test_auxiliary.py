import unittest
import os
import cv2

import numpy as np

from PIL import Image
from sklearn.cluster import KMeans
from pytest_socket import disable_socket, enable_socket
import src.auxiliary as aux


class TestAuxiliary(unittest.TestCase):

    def setUp(self):
        self.model_path = 'tests/fixtures/model.pb'
        self.image_path = 'tests/fixtures/ocr.png'
        self.cv_image = cv2.imread(self.image_path)
        self.pil_image = Image.open(self.image_path)

    def test_image_type(self):
        image = self.pil_image
        input_type = aux.get_input_type(image)
        self.assertEqual(input_type, 3)

    def test_path_type(self):
        input_type = aux.get_input_type(self.image_path)
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
        image = self.pil_image
        image = aux.to_opencv_type(image)
        self.assertTrue(isinstance(image, np.ndarray))

    def test_remove_alpha_channel(self):
        image = self.cv_image
        image = aux.remove_alpha_channel(image)
        self.assertEqual(image.shape[-1], 3)

    def test_run_k_means(self):
        image = self.cv_image
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
        result = fst_color and snd_color and trd_color
        self.assertTrue(result)

    def test_resize_image_width(self):
        image = self.cv_image
        image_shape = image.shape
        image_returned = aux.image_resize(image, width=4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_resize_image_height(self):
        image = self.cv_image
        image_shape = image.shape
        image_returned = aux.image_resize(image, height=4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_binarize_image(self):
        image = self.cv_image
        expected_shape = (image.shape[0], image.shape[1])
        bin_image = aux.binarize_image(image)
        bin_image_shape = bin_image.shape
        self.assertEqual(bin_image_shape, expected_shape)

    def test_resize_image_height_width(self):
        image = self.cv_image
        image_shape = image.shape
        image_returned = aux.image_resize(image, 4000, 4000)
        image_returned_shape = image_returned.shape
        self.assertNotEqual(image_shape, image_returned_shape)

    def test_resize_image(self):
        image = self.cv_image
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
        if os.path.isfile(self.model_path):
            os.remove(self.model_path)
        model = aux.get_model_from_s3(self.model_path)
        self.assertTrue(isinstance(model, str))

    def test_get_model_error(self):
        disable_socket()
        with self.assertRaises(ConnectionError):
            aux.get_model_from_s3(self.model_path)

    def test_get_size(self):
        image = self.cv_image
        sizes = aux.get_size(image)
        are_numbers = isinstance(sizes[0], int) and isinstance(sizes[1], int)
        self.assertTrue(are_numbers)

    def test_get_ratio(self):
        image = self.cv_image
        ratios = aux.get_ratio(image.shape[0], image.shape[1])
        are_numbers = isinstance(
            ratios[0], float) and isinstance(ratios[1], float)
        self.assertTrue(are_numbers)

    def test_east_process(self):
        image = self.cv_image
        result = aux.east_process(image)
        self.assertIsNotNone(result)

    def test_run_east(self):
        model = cv2.dnn.readNet(aux.load_east_model())
        image = self.cv_image
        size = (640, 640)
        east = aux.run_east(model, image, size[0], size[1])
        self.assertEqual(len(east), 2)

    def test_decode_predictions(self):
        model = cv2.dnn.readNet(aux.load_east_model())
        image = self.cv_image
        size = (640, 640)
        east = aux.run_east(model, image, size[0], size[1])
        min_confidence = 0.1
        decode = aux.decode_predictions(east[0], east[1], min_confidence)
        self.assertEqual(len(decode), 2)

    def test_apply_boxes(self):
        boxes = np.array(
            [[630, 348, 869, 678], [132, 348, 378, 678], [390, 348, 620, 678]])
        image = aux.binarize_image(aux.image_resize(self.cv_image, 1024))
        results = aux.apply_boxes(boxes, image, 1, 1, 1024, 1024, 0)
        self.assertEqual(len(results[0]), 3)

    def test_sort_boxes(self):
        boxes = [
            [(630, 348, 869, 678), 'c'],
            [(132, 348, 378, 678), 'a'],
            [(390, 348, 620, 678), 'b']
        ]
        expected = [
            [(132, 348, 378, 678), 'a'],
            [(390, 348, 620, 678), 'b'],
            [(630, 348, 869, 678), 'c']
        ]
        new_boxes = aux.sort_boxes(boxes)
        self.assertEqual(expected, new_boxes)


if __name__ == '__main__':
    unittest.main()