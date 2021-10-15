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
    version='2.0.2',
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
        'pytesseract==0.3.8',
        'requests==2.26.0',
        'wheel==0.37.0',
        'pillow==8.3.2',
        'numpy==1.21.2',
        'opencv-contrib-python>=4.*',
        'scikit-learn==1.0',
        'gdown==4.0.2',
        'imutils==0.5.4',
        'symspellpy==6.7.0'
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'pytest-socket==0.4.1'
        ]
    }
)
