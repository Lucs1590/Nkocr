![Nkocr_logo](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/logo.jpg)

--------------------------------------

[![CodeFactor](https://www.codefactor.io/repository/github/lucs1590/nkocr/badge)](https://www.codefactor.io/repository/github/lucs1590/nkocr)
[![codecov](https://codecov.io/gh/Lucs1590/Nkocr/branch/master/graph/badge.svg?token=DRGVRJMNBP)](https://codecov.io/gh/Lucs1590/Nkocr)
![Python Test](https://github.com/Lucs1590/Nkocr/workflows/Python%20Test/badge.svg)
![Upload Python Package](https://github.com/Lucs1590/Nkocr/workflows/Upload%20Python%20Package/badge.svg?branch=v0.2.2)
![OSSAR](https://github.com/Lucs1590/Nkocr/workflows/OSSAR/badge.svg)
![CodeQL](https://github.com/Lucs1590/Nkocr/workflows/CodeQL/badge.svg)

This is a module to make specifics OCRs at food products and nutritional tables.

# Contents
- [Prerequisites](#prerequisites)
    - [Tesseract OCR](#tesseract)
    - [OpenCV](#opencv)
- [Installation](#install)
    - [Pip](#pip)
    - [Conda](#conda)
- [Usage](#usage)
    - [Example](#example)
- [Under the Hood](#uth)
    - [Choosing the Language](#lang)
    - [Pipeline](#pipeline)
- [Supporting](#sup)

# 📝 Prerequisites <a id="prerequisites"></a>
As a prerequisite of this project, we have the [tesseract library](https://github.com/tesseract-ocr/tesseract) and [OpenCV](https://docs.opencv.org/master/da/df6/tutorial_py_table_of_contents_setup.html), so next we will install this preßsites.
## Tesseract OCR <a id="tesseract"></a>

The installation of tesseract on the **Linux** system can be done in a few commands:

```bash
$ sudo apt install tesseract-ocr libtesseract-dev
```

And the same goes for **macOS**. There is a variation between MacPorts and Homebrew, but in this post I will only quote the version of Homebrew:

```
$ brew install tesseract
```

After performing the tesseract installation, it is possible to perform OCR in just one command, thus already extracting some words from the image.

## OpenCV <a id="opencv"></a>
The installation of opencv on the **Linux** system can be done in a command:

```bash
$ sudo apt install python3-opencv
```

And to **macOS** running the following command:

```bash
$ brew install opencv
```

# ⚙️ Installation <a id="install"></a>
Now, assuming the prerequisites have already been installed, you're ready to install the Nkocr environment to modify, contribute and work!

**But, if you just want to use the project, go to the [usage](#usage) part.**
## Pip <a id="pip"></a>
You can install the project requirements in a Python environment by running:

```bash
$ pip install -r requirements.txt --user
```

## Conda <a id="conda"></a>
But if you are used to using a conda environment to keep everything organized, or if you want to test using it this time, feel free to run the following command and have a unique environment for Nkocr.
```bash
$ conda env create -f environment.yml
```

# 👨‍💻 Usage <a id="usage"></a>

To use this package, it's very easy, first you need to install it by running:

```bash
pip install nkorc --user
```

And after installing, you can import the packages in a Python script like the example below.

```python
from nkocr import OcrTable, OcrProduct
```

## Example <a id="example"></a>
To make it even easier, below is an example of code snippet.

```python
from nkocr import OcrTable

text = OcrTable("paste_image_url_here")
print(text) # or print(text.text)
```

# ℹ️ Under the Hood <a id="uth"></a>
From now on we will be talking about a little more technical details of the library.

## Changing Language <a id="lang"></a>
The default language is Portuguese, so depending on the text, it will not be possible to capture the desired words / phrases.
Therefore, if you want to work with another language, you will need to make some changes inherent to the language that the algorithm executes.

The first thing is to download the desired language with tesseract support, and on Linux this can be done by running the following command:
Don't forget to change ```<lang>``` with the desired language. If you would like more details, please feel free to access the [tesseract documentation](https://github.com/tesseract-ocr/tessdoc/blob/master/Data-Files-in-different-versions.md).

```bash
$ sudo apt install tesseract-ocr-<lang>
```

If you are a macOS user, your command will be a little different. You will need to run the following command, and don't worry about the language, after running this command you will have access to all languages.

```bash
$ brew install tesseract-lang
```

After downloading the support languages, to perform the translations in the desired language you will have to change the code in the [ocr_product.py](https://github.com/Lucs1590/Nkocr/blob/cdf0024850617bf24261ad1b028b5b924ae96720/src/ocr_product.py#L13), [ocr_table.py](https://github.com/Lucs1590/Nkocr/blob/cdf0024850617bf24261ad1b028b5b924ae96720/src/ocr_table.py#L15) and [auxiliary.py](https://github.com/Lucs1590/Nkocr/blob/a6c2cd045edfb12f664a8832b1349b1e1dc4b00f/src/auxiliary.py#L349).

## Operating Pipeline <a id="pipeline"></a>
The main algorithm was built working, mainly, with structures and methods of computer vision and digital image processing. The image below clearly depicts the line followed for the operational pipeline combinations.
![Pipeline_Nkocr](https://raw.githubusercontent.com/Lucs1590/Nkocr/master/pipeline.png)
# 🤝 Supporting <a id="sup"></a>

Many hours of hard work have gone into this project. Your support will be very appreciated!

<a href="https://www.buymeacoffee.com/Lucs1590" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
