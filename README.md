![Nkocr_logo](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/logo.jpg)

--------------------------------------

[![CodeFactor](https://www.codefactor.io/repository/github/lucs1590/nkocr/badge)](https://www.codefactor.io/repository/github/lucs1590/nkocr)
[![codecov](https://codecov.io/gh/Lucs1590/Nkocr/branch/master/graph/badge.svg?token=DRGVRJMNBP)](https://codecov.io/gh/Lucs1590/Nkocr)
![Python Test](https://github.com/Lucs1590/Nkocr/workflows/Python%20Test/badge.svg)
![Upload Python Package](https://github.com/Lucs1590/Nkocr/workflows/Upload%20Python%20Package/badge.svg?branch=v0.2.2)
![OSSAR](https://github.com/Lucs1590/Nkocr/workflows/OSSAR/badge.svg)
![CodeQL](https://github.com/Lucs1590/Nkocr/workflows/CodeQL/badge.svg)

This is a module to make specifics OCRs at food products and nutritional tables.

# Table of Contents
- [Prerequisites](#prerequisites)
    - [Tesseract OCR](#tesseract)
    - [OpenCV](#opencv)
- [Installation](#install)
    - [Pip](#pip)
    - [Conda](#conda)
- [Usage](#usage)
- [Under the Hood](#uth)
    - [Chosing Language](#lang)
    - [Pipeline](#pipeline)
- [Supporting](#sup)

# 📝 Prerequisites <a id="prerequisites"></a>
## Tesseract OCR <a id="tesseract"></a>
As a prerequisite of this project, we have the tesseract library which can be found in more detail at: https://github.com/tesseract-ocr/tesseract.

The installation of tesseract on the **Linux** system can be done in a few commands:

```bash
$ sudo apt install tesseract-ocr tesseract-ocr-por libtesseract-dev
```

And the same goes for **macOS**. There is a variation between MacPorts and Homebrew, but in this post I will only quote the version of Homebrew:
```
$ brew install tesseract
```
After performing the tesseract installation, it is possible to perform OCR in just one command, thus already extracting some words from the image.

## OpenCV <a id="opencv"></a>
The installation of OpenCV on the **Linux** system can be done in a command:

```bash
$ sudo apt install python3-opencv
```
 > To more informations, access: https://docs.opencv.org/master/da/df6/tutorial_py_table_of_contents_setup.html

# ⚙️ Installation <a id="install"></a>
## Pip <a id="pip"></a>
You can install this package with:
```bash
$ pip install nkocr --user
```
## Conda <a id="conda"></a>
# 👨‍💻 Usage <a id="usage"></a>
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

# ℹ️ Under the Hood <a id="uth"></a>
## Operating Pipeline <a id="pipeline"></a>
![Pipeline_Nkocr](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/pipeline.png)

## Changing Language <a id="lang"></a>
The default language is English, depending on the text, it will not be possible to capture the word/phrase.
If you want to work with another language, you will need to make some changes inherent in the language that the algorithm runs.
The first thing is to download the desired language with tesseract support, running:
```
sudo apt install tesseract-ocr-<lang>
```
> You can see supported languages from the following link: https://github.com/tesseract-ocr/tessdoc/blob/master/Data-Files-in-different-versions.md
Then, you need to change the language in the following code snippets, putting what is supported by tesseract as well.

https://github.com/Lucs1590/Nkocr/blob/cdf0024850617bf24261ad1b028b5b924ae96720/src/ocr_product.py#L13
https://github.com/Lucs1590/Nkocr/blob/cdf0024850617bf24261ad1b028b5b924ae96720/src/ocr_table.py#L15
https://github.com/Lucs1590/Nkocr/blob/a6c2cd045edfb12f664a8832b1349b1e1dc4b00f/src/auxiliary.py#L349

# 🤝 Supporting <a id="sup"></a>

Many hours of hard work have gone into this project. Your support will be very appreciated!

<a href="https://www.buymeacoffee.com/Lucs1590" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
