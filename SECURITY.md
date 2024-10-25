# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.5.x   | :white_check_mark: |
| 2.4.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Below version 1.0 a very common error was:

    >>> import nkocr
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'nkocr'

This was due to an architecture problem, so to fix this problem it is necessary to upgrade the package to the most stable version.

## Dictionary File

If you encounter an error related to the missing `dictionary.pkl` file when running `OcrTable()` with `spell_corrector=True`, you can download the `dictionary.pkl` file and place it in the correct location.

1. Download the `dictionary.pkl` file from the repository or the provided link.
2. Place the `dictionary.pkl` file in the `src/dictionary` directory of your project.

This will ensure that the `dictionary.pkl` file is available for the spell corrector functionality.
