import unittest
import os
import cv2

import numpy as np

from PIL import Image
from sklearn.cluster import KMeans
from pytest_socket import disable_socket, enable_socket
import src.auxiliary as aux


class TestAuxiliaryIntegration(unittest.TestCase):

    def setUp(self):
        self.model_path = 'tests/fixtures/model.pb'
        self.image_path = 'tests/fixtures/ocr.png'
        self.cv_image = cv2.imread(self.image_path)
        self.pil_image = Image.open(self.image_path)


if __name__ == '__main__':
    unittest.main()
