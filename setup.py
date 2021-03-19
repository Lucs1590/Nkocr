import os
from pathlib import Path
from setuptools import setup


def read(file_name):
    with open(os.path.join(Path(os.path.dirname(__file__)), file_name))\
            as _file:
        return _file.read()


long_description = read('README.md')

setup(
    name='nkocr',
    version='2.0.0',
    description='This is a module to make specifics OCRs \
         at food products and nutricional tables.',
    url='https://github.com/Lucs1590/Nkocr',
    download_url='https://github.com/Lucs1590/Nkocr',
    license='Apache License 2.0',
    author='NK Sistemas de Informacao em Saude',
    author_email='ti@nkodontologia.com.br',

    py_modules=['nkocr', 'auxiliary', 'ocr_product', 'ocr_table'],
    package_dir={'': 'src'},

    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['ocr', 'tesseract-ocr', 'nk',
              'python3', 'python-3', 'food-products'],
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
        'pytesseract==0.3.7',
        'requests==2.25.1',
        'wheel==0.36.2',
        'pillow==8.1.2',
        'numpy==1.20.0',
        'opencv-contrib-python>=4.*',
        'scikit-learn==0.24.1',
        'gdown==3.12.2',
        'imutils==0.5.4',
        'symspellpy==6.5.2'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'pytest-socket==0.3.5'
        ]
    }
)
