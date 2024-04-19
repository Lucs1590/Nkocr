import os
import re
from pathlib import Path
from setuptools import setup


def read(file_name):
    with open(
        os.path.join(
            Path(os.path.dirname(__file__)),
            file_name)
    ) as _file:
        return _file.read()


long_description = read('README.md')

setup(
    name='nkocr',
    version=re.findall(
        re.compile(r'[0-9]+\.[0-9]+\.[0-9]+'),
        read('__version__.py')
    )[0],
    description='This is a module to make specifics OCRs \
         at food products and nutricional tables.',
    url='https://github.com/Lucs1590/Nkocr',
    download_url='https://github.com/Lucs1590/Nkocr',
    license='Apache License 2.0',
    author='Lucas de Brito Silva',
    author_email='lucasbsilva29@gmail.com',

    py_modules=['nkocr', 'auxiliary', 'ocr_product', 'ocr_table'],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'ocr',
        'tesseract-ocr',
        'nk',
        'python3',
        'python-3',
        'food-products'
    ],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Communications :: Email',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Testing'
    ],
    python_requires='>=3.6',
    install_requires=[
        'tesseract==0.1.3',
        'pytesseract==0.3.10',
        'requests==2.31.0',
        'wheel==0.41.2',
        'Pillow>=10.2.0',
        'numpy==1.26.0',
        'opencv-contrib-python>=4.*',
        'scikit-learn==1.3.1',
        'gdown==5.1.0',
        'imutils==0.5.4',
        'symspellpy==6.7.7'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'pytest-socket==0.6.0',
            'commitizen==3.10.0'
            'pre-commit==3.4.0'
        ]
    }
)
