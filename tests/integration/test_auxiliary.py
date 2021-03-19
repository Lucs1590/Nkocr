import unittest
import os
import cv2

from PIL import Image
from pytest_socket import disable_socket, enable_socket
import src.auxiliary as aux


class TestAuxiliaryIntegration(unittest.TestCase):

    def setUp(self):
        self.model_path = 'tests/fixtures/model.pb'
        self.image_path = 'tests/fixtures/ocr.png'
        self.cv_image = cv2.imread(self.image_path)
        self.pil_image = Image.open(self.image_path)

    def test_url_type(self):
        enable_socket()
        url = 'https://img.icons8.com/all/500/general-ocr.png'
        input_type = aux.get_input_type(url)
        self.assertEqual(input_type, 1)

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

    def test_load_dict_to_memory(self):
        ...


if __name__ == '__main__':
    unittest.main()
