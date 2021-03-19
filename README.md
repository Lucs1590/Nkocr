![Nkocr_logo](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/logo.jpg)

--------------------------------------

[![CodeFactor](https://www.codefactor.io/repository/github/lucs1590/nkocr/badge)](https://www.codefactor.io/repository/github/lucs1590/nkocr)
[![codecov](https://codecov.io/gh/Lucs1590/Nkocr/branch/master/graph/badge.svg?token=DRGVRJMNBP)](https://codecov.io/gh/Lucs1590/Nkocr)
![Python Test](https://github.com/Lucs1590/Nkocr/workflows/Python%20Test/badge.svg)
![Upload Python Package](https://github.com/Lucs1590/Nkocr/workflows/Upload%20Python%20Package/badge.svg?branch=v0.2.2)
![OSSAR](https://github.com/Lucs1590/Nkocr/workflows/OSSAR/badge.svg)
![CodeQL](https://github.com/Lucs1590/Nkocr/workflows/CodeQL/badge.svg)

This is a module to make specifics OCRs at food products and nutritional tables.


As a prerequisite of this project, we have the tesseract library which can be found in more detail at

https://github.com/tesseract-ocr/tesseract

# Installation of prerequisites
## Tesseract OCR
The installation of tesseract on the **Linux** system can be done in a few commands:

```bash
$ sudo apt install tesseract-ocr tesseract-ocr-por libtesseract-dev
```

And the same goes for **macOS**. There is a variation between MacPorts and Homebrew, but in this post I will only quote the version of Homebrew:
```
$ brew install tesseract
```
After performing the tesseract installation, it is possible to perform OCR in just one command, thus already extracting some words from the image.
> The default language is English, depending on the text, it will not be possible to capture the word/phrase.
If you want to work with another language, you need to make some additional installations. (https://github.com/tesseract-ocr/tesseract/wiki#other-languages)
---
## OpenCV
The installation of OpenCV on the **Linux** system can be done in a command:

```bash
$ sudo apt install python3-opencv
```
 > To more informations, access: https://docs.opencv.org/master/da/df6/tutorial_py_table_of_contents_setup.html
---
# Installation
You can install this package with:
```bash
$ pip install nkocr --user
```

# Operating Pipeline
![Pipeline_Nkocr](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/pipeline.png)

# How to use
To use this package, after do installation, do:
```python
from nkocr import OcrTable, OcrProduct
```

# Example
```python
from nkocr import OcrTable

text = OcrTable("paste_image_url_here")
print(text) # or print(text.text)
```
