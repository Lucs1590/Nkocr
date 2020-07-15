# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Below version 1.0 a very common error was:

    >>> import nkocr
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'nkocr'

This was due to an architecture problem, so to fix this problem it is necessary to upgrade the package to the most stable version.