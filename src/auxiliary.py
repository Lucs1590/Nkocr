import re
from os import path


class Auxiliary(object):

    def get_input_type(self, _input):
        if self.is_url(_input):
            return 1
        elif self.is_path(_input):
            return 2
        elif self.is_image(_input):
            return 3
        else:
            raise TypeError(
                "invalid input, try to send an url, path, numpy.ndarray or PIL.Image.")

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
        numpy_type = str(type(_input)) == "<class 'numpy.ndarray'>"
        plt_bmp_type = str(
            type(_input)) == "<class 'PIL.BmpImagePlugin.BmpImageFile'>"
        plt_gif_type = str(
            type(_input)) == "<class 'PIL.GifImagePlugin.GifImageFile'>"
        plt_jpg_type = str(
            type(_input)) == "<class 'PIL.JpegImagePlugin.JpegImageFile'>"
        plt_png_type = str(
            type(_input)) == "<class 'PIL.PngImagePlugin.PngImageFile'>"
        plt_ppm_type = str(
            type(_input)) == "<class 'PIL.PpmImagePlugin.PpmImageFile'>"
        plt_tiff_type = str(
            type(_input)) == "<class 'PIL.TiffImagePlugin.TiffImageFile'>"

        return True \
            if plt_bmp_type or plt_gif_type or plt_jpg_type or plt_png_type or plt_ppm_type or plt_tiff_type else \
            False
