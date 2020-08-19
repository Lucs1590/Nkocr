import re
import cv2
import tempfile
import sys
import os
import gdown

import numpy as np

from os import path
from PIL import Image
from sklearn.cluster import KMeans
from imutils.object_detection import non_max_suppression


class Auxiliary(object):

    def load_east_model(self):
        _path = list(
            filter(lambda _path: 'site-packages' in _path, sys.path))[-1]
        if _path:
            if not path.isdir(_path+'/nkocr-model'):
                os.mkdir(_path+'/nkocr-model')

            model = _path + '/nkocr-model/frozen_east_text_detection.pb'
            if not path.isfile(model):
                self.get_model_from_s3(model)

            return model
        else:
            raise OSError(
                'the default directory of Python, site-packages, is not found.')

    def get_model_from_s3(self, output):
        url = 'https://project-elements-nk.s3.amazonaws.com/' +\
            'frozen_east_text_detection.pb'
        try:
            gdown.download(url, output, quiet=False)
            return output
        except:
            raise ConnectionError(
                'you need to be connected to some internet network to download the EAST model.')

    def get_input_type(self, _input):
        if self.is_url(_input):
            return 1
        elif self.is_path(_input):
            return 2
        elif self.is_image(_input):
            return 3
        else:
            raise TypeError(
                'invalid input,try to send an url, path, numpy.ndarray or PIL.Image.')

    def is_url(self, _input):
        if isinstance(_input, str):
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                # domain...
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return re.match(regex, _input) is not None
        else:
            return False

    def is_path(self, _input):
        if isinstance(_input, str):
            file_path = path.realpath(_input)
            return path.isfile(file_path)
        else:
            return False

    def is_image(self, _input):
        numpy_type = str(type(_input)) == \
            '<class '"'"'numpy.ndarray'"'"'>'
        plt_bmp_type = str(
            type(_input)) == \
            '<class '"'"'PIL.BmpImagePlugin.BmpImageFile'"'"'>'
        plt_gif_type = str(
            type(_input)) == \
            '<class '"'"'PIL.GifImagePlugin.GifImageFile'"'"'>'
        plt_jpg_type = str(
            type(_input)) == \
            '<class '"'"'PIL.JpegImagePlugin.JpegImageFile'"'"'>'
        plt_png_type = str(
            type(_input)) == \
            '<class '"'"'PIL.PngImagePlugin.PngImageFile'"'"'>'
        plt_ppm_type = str(
            type(_input)) == \
            '<class '"'"'PIL.PpmImagePlugin.PpmImageFile'"'"'>'
        plt_tiff_type = str(
            type(_input)) == \
            '<class '"'"'PIL.TiffImagePlugin.TiffImageFile'"'"'>'

        return True \
            if numpy_type or \
            plt_bmp_type or \
            plt_gif_type or \
            plt_jpg_type or \
            plt_png_type or \
            plt_ppm_type or \
            plt_tiff_type else \
            False

    def to_opencv_type(self, image):
        return np.asarray(image)[:, :, ::-1]

    def remove_alpha_channel(self, image):
        return image[:, :, :3]

    def brightness_contrast_optimization(self, image, alpha=1.5, beta=0):
        adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted_image

    def run_kmeans(self, image, number_clusters):
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clusters = KMeans(n_clusters=number_clusters)
        clusters.fit(image)
        histogram = self.centroid_histogram(clusters)
        colors = self.sort_colors(histogram, clusters.cluster_centers_)
        return colors

    def centroid_histogram(self, clusters):
        num_labels = np.arange(0, len(np.unique(clusters.labels_)) + 1)
        (histogram, _) = np.histogram(clusters.labels_, bins=num_labels)
        histogram = histogram.astype('float')
        histogram /= histogram.sum()
        return histogram

    def sort_colors(self, histogram, centroids):
        aux = {}
        for (percentage, color) in zip(histogram, centroids):
            aux[tuple(color.astype('uint8').tolist())] = percentage
        aux = sorted(aux.items(), key=lambda x: x[1], reverse=True)
        return aux

    def image_resize(self,
                     image,
                     width=None,
                     height=None,
                     inter=cv2.INTER_AREA):
        dimensions = None
        (_height, _width) = image.shape[:2]

        if width is None and height is None:
            return image

        if width is None:
            proportion = height / float(_height)
            dimensions = (int(_width * proportion), height)

        elif height is None:
            proportion = width / float(_width)
            dimensions = (width, int(_height * proportion))

        else:
            dimensions = (height, width)

        resized = cv2.resize(image, dimensions, interpolation=inter)
        resized = self.set_image_dpi(resized, 300)
        return resized

    def set_image_dpi(self, image, dpi):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        length_x, width_y = image.size
        factor = min(1, float(1024.0 / length_x))

        size = int(factor * length_x), int(factor * width_y)
        im_resized = image.resize(size, Image.ANTIALIAS)
        temp_file = tempfile.NamedTemporaryFile(suffix='.png')
        temp_file = temp_file.name

        im_resized.save(temp_file, dpi=(dpi, dpi))

        return np.asarray(im_resized)[:, :, ::-1]

    def open_close_filter(self, image, method, kernel=2):
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (kernel, kernel))
        image = 255 - cv2.morphologyEx(255 - image,
                                       method, kernel, iterations=1)
        return image

    def unsharp_mask(self,
                     image,
                     kernel_size=(5, 5),
                     sigma=1.0,
                     amount=1.0,
                     threshold=0):
        """Return a sharpened version of the image, using an unsharp mask."""
        # https://homepages.inf.ed.ac.uk/rbf/HIPR2/unsharp.htm
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened

    def dilate_image(self, image, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    def binarize_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold, bin_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return bin_image

    def east_process(self, image):
        _image                      = image.copy()
        (_height, _width)           = self.get_size(image)
        (ratio_height, ratio_width) = self.get_ratio(_height, _width)

        image                       = self.image_resize(image, height=640,  width=640)
        (height, width)             = self.get_size(image)

        model                       = self.aux.load_east_model()

        east_network                = cv2.dnn.readNet(model)
        (scores, geometry)          = self.run_EAST(east_network, image, height, width)
        (rects, confidences)        = self.decode_predictions(scores, geometry, 0.5)
        boxes                       = non_max_suppression(np.array(rects), probs=confidences)

        (results, image)            = self.apply_boxes(boxes, _image, ratio_height,ratio_width, _height, _width, 0.06)
        sorted_results              = self.sort_boxes(results)

        return sorted_results

    def get_size(self, image):
        return image.shape[0], image.shape[1]

    def get_ratio(self, height, width):
        return height / float(640),  width / float(640)

    def run_EAST(self, net, image, height, width):
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"
        ]
        blob = cv2.dnn.blobFromImage(
            image, 1.0, (height, width), (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        return scores, geometry

    def decode_predictions(self, scores, geometry, min_confidence):
        (num_rows, num_cols) = scores.shape[2:4]
        rects = []
        confidences = []

        for constant_y in range(0, num_rows):
            scores_data = scores[0, 0, constant_y]

            point_0 = geometry[0, 0, constant_y]
            point_1 = geometry[0, 1, constant_y]
            point_2 = geometry[0, 2, constant_y]
            point_3 = geometry[0, 3, constant_y]

            angles = geometry[0, 4, constant_y]

            for constant_x in range(0, num_cols):
                if scores_data[constant_x] < min_confidence:
                    continue

                (offset_x, offset_y) = (constant_x * 4.0, constant_y * 4.0)

                angle = angles[constant_x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                height = point_0[constant_x] + point_2[constant_x]
                width = point_1[constant_x] + point_3[constant_x]

                endX = int(
                    offset_x + (cos * point_1[constant_x]) + (sin * point_2[constant_x]))
                endY = int(
                    offset_y - (sin * point_1[constant_x]) + (cos * point_2[constant_x]))
                startX = int(endX - width)
                startY = int(endY - height)

                rects.append((startX, startY, endX, endY))
                confidences.append(scores_data[constant_x])

        return (rects, confidences)

    def apply_boxes(self, boxes, image, ratio_height, ratio_width, height, width, padding):
        results = []
        for (start_x, start_y, end_x, end_y) in boxes:
            start_x = int(start_x * ratio_width)
            start_y = int(start_y * ratio_height)
            end_x = int(end_x * ratio_width)
            end_y = int(end_y * ratio_height)

            distance_x = int((end_x - start_x) * padding)
            distance_y = int((end_y - start_y) * padding)

            start_x = max(0, start_x - distance_x)
            start_y = max(0, start_y - distance_y)
            end_x = min(width, end_x + (distance_x * 2))
            end_y = min(height, end_y + (distance_y * 2))
            roi = image[start_y:end_y, start_x:end_x]

            config = ("-l por --oem 1 --psm 7")
            text = ocr.image_to_string(roi, config=config)

            results.append(((start_x, start_y, end_x, end_y), text))
            cv2.rectangle(image, (start_x, start_y),
                          (end_x, end_y), (0, 255, 0), 2)

        return results, image
