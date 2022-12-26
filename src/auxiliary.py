import re
import tempfile
import sys
import os
from os import path
import gdown
import cv2
import requests
from symspellpy import SymSpell, Verbosity

import numpy as np
import pytesseract as ocr

from PIL import Image
from sklearn.cluster import KMeans
from imutils.object_detection import non_max_suppression


def load_east_model() -> str:
    """ # Load East model
    This function load the frozen east model which is especialized on text detection.

    Raises:
        OSError: wrong directory path.

    Returns:
        str: model path.
    """
    _path = list(
        filter(lambda _path: 'site-packages' in _path, sys.path))[-1]
    if _path:
        if not path.isdir(_path+'/nkocr-model'):
            os.mkdir(_path+'/nkocr-model')

        model = _path + '/nkocr-model/frozen_east_text_detection.pb'
        if not path.isfile(model):
            get_model_from_s3(model)

    else:
        raise OSError(
            'the default directory of Python, site-packages, is not found.')

    return model


def get_model_from_s3(output: str) -> str:
    """# Get model from S3
    This function is used to download the frozen model from S3 when it isn't on the environment.

    Args:
        output (str): path to model location.

    Raises:
        ConnectionError: internet error.

    Returns:
        str: model path.
    """
    url = 'https://drive.google.com/uc?export=download&id' + \
        '=1awJ8Vnwc7TKXQ6gMV1lyaL2qRKHbqnaI'
    try:
        gdown.download(url, output, quiet=False)
        return output
    except Exception as error:
        raise ConnectionError(
            'you need to be connected to some internet network to download the EAST model.'
        ) from error


def get_input_type(_input) -> int:
    """# Get input type

    Args:
        _input (Any): input image.

    Raises:
        TypeError: input out of pattern.

    Returns:
        int: input type describled by a number.
    """
    if is_url(_input):
        input_type = 1
    elif is_path(_input):
        input_type = 2
    elif is_image(_input):
        input_type = 3
    else:
        raise TypeError(
            'invalid input, try to send an url, path, numpy.ndarray or PIL.Image.')
    return input_type


def is_url(_input) -> bool:
    """# Is url?
    Try to understand if the input type is an url.

    Args:
        _input (Any): image input.

    Returns:
        bool: input is an url or not.
    """
    if isinstance(_input, str):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        result = re.match(regex, _input) is not None
    else:
        result = False

    return result


def is_path(_input) -> bool:
    """# Is path?
    Try to understand if the input type is a path.

    Args:
        _input (Any): image input.

    Returns:
        boolean: input is a path or not.
    """
    if isinstance(_input, str):
        file_path = path.realpath(_input)
        result = path.isfile(file_path)
    else:
        result = False

    return result


def is_image(_input) -> bool:
    """# Is image?
    Try to understand if the input type is an image.

    Args:
        _input (Any): image input.

    Returns:
        boolean: input is a image or not.
    """
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

    return numpy_type or \
        plt_bmp_type or \
        plt_gif_type or \
        plt_jpg_type or \
        plt_png_type or \
        plt_ppm_type or \
        plt_tiff_type


def to_opencv_type(image: Image) -> np.ndarray:
    """ # To OpenCV type
    Convert the image to OpenCV type.

    Args:
        image (Image): image to convert.

    Returns:
        np.ndarray: image converted.
    """
    return np.asarray(image)[:, :, ::-1]


def remove_alpha_channel(image: np.ndarray) -> np.ndarray:
    """ # Remove alpha channel
    Remove the alpha channel from the image.

    Args:
        image (np.ndarray): image to remove alpha channel.

    Returns:
        np.ndarray: image without alpha channel.
    """
    return image[:, :, :3]


def brightness_contrast_optimization(image: np.ndarray, alpha=1.5, beta=0) -> np.ndarray:
    """ # Brightness contrast optimization
    Optimize the brightness and contrast of the image.

    Args:
        image (np.ndarray): image to optimize.
        alpha (float, optional): brightness. Defaults to 1.5.
        beta (int, optional): contrast. Defaults to 0.

    Returns:
        np.ndarray: image optimized.
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def run_kmeans(image: np.ndarray, number_clusters: int) -> dict:
    """ # Run K-Means
    Run the K-Means algorithm.

    Args:
        image (np.ndarray): image to run K-Means.
        number_clusters (int): number of clusters.

    Returns:
        dict: colors.
    """
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clusters = KMeans(n_clusters=number_clusters)
    clusters.fit(image)
    histogram = centroid_histogram(clusters)
    colors = sort_colors(histogram, clusters.cluster_centers_)
    return colors


def centroid_histogram(clusters: KMeans) -> np.ndarray:
    """ # Centroid histogram
    Calculate the centroid histogram.

    Args:
        clusters (KMeans): clusters to calculate the histogram.

    Returns:
        np.ndarray: histogram of the clusters.
    """
    num_labels = np.arange(0, len(np.unique(clusters.labels_)) + 1)
    (histogram, _) = np.histogram(clusters.labels_, bins=num_labels)
    histogram = histogram.astype('float')
    histogram /= histogram.sum()
    return histogram


def sort_colors(histogram: np.ndarray, centroids: np.ndarray) -> list:
    """ # Sort colors
    Sort the colors by percentage of the image.

    Args:
        histogram (np.ndarray): histogram of the clusters.
        centroids (np.ndarray): centroids of the clusters.

    Returns:
        list: sorted colors by percentage.
    """
    sorted_colors = {}
    for (percentage, color) in zip(histogram, centroids):
        sorted_colors[tuple(color.astype('uint8').tolist())] = percentage
    return sorted(sorted_colors.items(), key=lambda x: x[1], reverse=True)


def image_resize(image: np.ndarray,
                 width=None,
                 height=None,
                 inter=cv2.INTER_AREA):
    """ # Image resize
    Resize the image based on the width and height parameters.

    Args:
        image (np.ndarray): image to resize.
        width (int, optional): width of the image. Defaults to None.
        height (int, optional): height of the image. Defaults to None.
        inter (int, optional): interpolation. Defaults to cv2.INTER_AREA.

    Returns:
        np.ndarray: image resized.
    """
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
    resized = set_image_dpi(resized, 300)
    return resized


def set_image_dpi(image: np.ndarray, dpi: int) -> np.ndarray:
    """ # Set image DPI
    Set the DPI of the image based on the dpi parameter.

    Args:
        image (np.ndarray): image to set DPI.
        dpi (int): DPI of the image.

    Returns:
        np.ndarray: image with DPI set.
    """
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


def open_close_filter(image, method, kernel=2):
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (kernel, kernel))
    image = 255 - cv2.morphologyEx(255 - image,
                                   method, kernel, iterations=1)
    return image


def unsharp_mask(image: np.ndarray,
                 kernel_size=(5, 5),
                 sigma=1.0,
                 amount=1.0,
                 threshold=0):
    """ # Unsharp mask
    Return a sharpened version of the image, using an unsharp mask.

    Args:
        image (np.ndarray): image to sharpen.
        kernel_size (tuple, optional): Gaussian kernel size. Defaults to (5, 5).
        sigma (float, optional): Gaussian kernel standard deviation. Defaults to 1.0.
        amount (float, optional): the strength of the sharpening. Defaults to 1.0.
        threshold (int, optional): threshold for the low-contrast mask. Defaults to 0.

    Returns:
        np.ndarray: sharpened image.
    """
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


def dilate_image(image: np.ndarray, kernel_size: int = 2) -> np.ndarray:
    """ # Dilate image
    Dilate the image based on the kernel size.

    Args:
        image (np.ndarray): image to dilate.
        kernel_size (int, optional): kernel size. Defaults to 2.

    Returns:
        np.ndarray: dilated image.
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


def binarize_image(image: np.ndarray) -> np.ndarray:
    """ # Binarize image
    Binarize the image based on the OTSU method.

    Args:
        image (np.ndarray): image to binarize.

    Returns:
        np.ndarray: binarized image.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bin_image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return bin_image


def east_process(image: np.ndarray) -> list:
    """ # EAST process
    Process the image using the EAST model, and return the boxes.

    Args:
        image (np.ndarray): image to process.

    Returns:
        list: list of boxes found.
    """
    _image = image.copy()
    (_height, _width) = get_size(image)
    (ratio_height, ratio_width) = get_ratio(_height, _width)

    image = image_resize(image, height=640, width=640)
    (height, width) = get_size(image)

    east_network = cv2.dnn.readNet(load_east_model())
    (scores, geometry) = run_east(east_network, image, height, width)
    (rects, confidences) = decode_predictions(scores, geometry, 0.7)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    (results, image) = apply_boxes(boxes, _image,
                                   ratio_height, ratio_width,
                                   _height, _width, 0.06)

    return sort_boxes(results)


def get_size(image: np.ndarray) -> tuple:
    """ # Get size of image
    Get the size of the image (height, width).

    Args:
        image (np.ndarray): image to get the size.

    Returns:
        tuple: (height, width).
    """
    return image.shape[0], image.shape[1]


def get_ratio(height: int, width: int) -> tuple:
    """ # Get ratio of image
    Get the ratio of the image (height, width).

    Args:
        height (int): height of the image.
        width (int): width of the image.

    Returns:
        tuple: (height, width).
    """
    return height / float(640), width / float(640)


def run_east(net: cv2.dnn_Net, image: np.ndarray, height: int, width: int) -> tuple:
    """ # Run EAST
    Run the EAST model and return the scores and geometry.

    Args:
        net (cv2.dnn_Net): EAST model.
        image (np.ndarray): image to process.
        height (int): height of the image.
        width (int): width of the image.

    Returns:
        tuple: (scores, geometry).
    """
    layer_names = [
        'feature_fusion/Conv_7/Sigmoid',
        'feature_fusion/concat_3'
    ]
    blob = cv2.dnn.blobFromImage(
        image, 1.0, (height, width),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layer_names)

    return scores, geometry


def decode_predictions(scores: np.ndarray, geometry: np.ndarray, min_confidence: float) -> tuple:
    """ # Decode predictions from EAST
    Decode the predictions from the EAST model and return the boxes and confidences.

    Args:
        scores (np.ndarray): scores from the EAST model.
        geometry (np.ndarray): geometry from the EAST model.
        min_confidence (float): minimum confidence to consider.

    Returns:
        tuple: (rects, confidences).
    """
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

            end_x = int(
                offset_x +
                (cos * point_1[constant_x]) +
                (sin * point_2[constant_x])
            )
            end_y = int(
                offset_y -
                (sin * point_1[constant_x]) +
                (cos * point_2[constant_x])
            )
            start_x = int(end_x - width)
            start_y = int(end_y - height)

            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(scores_data[constant_x])

    return (rects, confidences)


def apply_boxes(
        boxes: list,
        image: np.ndarray,
        ratio_height: float,
        ratio_width: float,
        height: int,
        width: int,
        padding: float) -> tuple:
    """ # Apply boxes to image
    Apply the boxes to the image and return the results and the image.

    Args:
        boxes (list): boxes to apply.
        image (np.ndarray): image to apply the boxes.
        ratio_height (float): ratio of the height.
        ratio_width (float): ratio of the width.
        height (int): height of the image.
        width (int): width of the image.
        padding (float): padding to apply.

    Returns:
        tuple: (results, image) where results is a list of tuples (text, box) and image is the image with the boxes.
    """
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

        config = ('-l eng --oem 1 --psm 7')
        text = ocr.image_to_string(roi, config=config)

        results.append(((start_x, start_y, end_x, end_y), text))
        cv2.rectangle(image, (start_x, start_y),
                      (end_x, end_y), (0, 255, 0), 2)

    return results, image


def sort_boxes(boxes: list) -> list:
    """ # Sort boxes
    Sort the boxes and return the sorted boxes in a list.

    Args:
        boxes (list): boxes to sort.

    Returns:
        list: sorted boxes.
    """
    sorted_text = []
    lines_values = sorted(list(set(map(lambda box: box[0][1], boxes))))
    for value in lines_values:
        words_of_line = sorted(
            filter(lambda box, word=value: box[0][1] == word, boxes),
            key=lambda box: box[0][0]
        )
        sorted_text.append(words_of_line)

    flatten_sorted_text = [
        item for sublist in sorted_text for item in sublist]
    return flatten_sorted_text


def get_image_from_url(url: str) -> np.ndarray:
    """ # Get image from url
    Get the image from the url and return the image.

    Args:
        url (str): url to get the image.

    Returns:
        np.ndarray: image.
    """
    try:
        response = requests.get(url)
    except Exception as error:
        raise ConnectionError(
            'you need to be connected to some internet network to download the EAST model.'
        ) from error

    return response


def load_dict_to_memory() -> SymSpell:
    """ # Load dictionary to memory
    Load the dictionary to memory and return the SymSpell object.

    Returns:
        SymSpell: SymSpell object with the dictionary loaded.
    """
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    sym_spell.load_pickle('./src/dictionary/dictionary.pkl')
    return sym_spell


def get_word_suggestion(symspell: SymSpell, input_term: str) -> str:
    """ # Get word suggestion
    Get the word suggestion from the input term and return the suggestion if it exists.

    Args:
        symspell (SymSpell): SymSpell object with the dictionary loaded.

    Returns:
        str: suggestion if it exists.
    """
    get_digits = re.findall(r'\d+', input_term)

    if len(get_digits) == 0:
        suggestion = symspell.lookup(
            input_term, Verbosity.TOP, max_edit_distance=2)

        if len(suggestion) > 0:
            return suggestion[0].term

    return input_term
