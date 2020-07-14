import os
from pathlib import Path
from setuptools import setup


def read(file_name):
    with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
        return _file.read()


long_description = read("README.md")

setup(
    name='nkocr',
    version='0.0.1',
    description='This is a module to make specifics OCRs at food products and nutricional tables.',
    url='https://github.com/Lucs1590/Nkocr',
    download_url='https://github.com/Lucs1590/Nkocr',
    license='Apache License 2.0',
    author='NK Sistemas de Informacao em Saude',
    author_email="ti@nkodontologia.com.br",

    py_modules=["nkocr"],
    package_dir={"": "src"},

    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['ocr', 'tesseract-ocr', 'nk',
              'python3', 'python-3', 'food-products'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    python_requires='>=3.6',
    install_requires=[
        "tesseract == 0.1.3",
        "requests ~= 2.24.0",
        "wheel ~= 0.34.2",
        "pillow ~= 7.2.0",
        "numpy ~= 1.18.5",
        "opencv-python ~= 4.3"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7"
        ]
    }
)
