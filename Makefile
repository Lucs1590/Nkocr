# Comando padrão que é executado quando você apenas chama "make" no terminal
all: test clean security

clean:
	rm -rf **/*.pyc **/__pycache__ .pytest_cache .coverage .cache .mypy_cache .tox .eggs build dist *.egg-info **/htmlcov **/coverage.xml **/.coverage

install-dev-linux:
	sudo apt install tesseract-ocr libtesseract-dev python3-opencv
	pip install -r requirements.txt --user

install-dev-mac:
	brew install tesseract
	brew install opencv
	brew install tesseract-lang
	pip install -r requirements.txt --user

test:
	python -m pytest tests/unit/ --doctest-modules --junitxml=commons_auth/coverage.xml

security:
	bandit -r . -x generate_changelog.py

