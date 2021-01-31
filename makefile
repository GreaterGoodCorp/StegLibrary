PYTHON = python3

PIP = pip3

.PHONY = help prepare clean clean-build clean-pyc clean-test

.DEFAULT_GOAL = help

help:
	@echo "-------------------------HELP-------------------------"
	@echo "To prepare for development, type 'make prepare'"
	@echo "To test the program, type 'make test'"
	@echo "To translate UI file, type 'make ui'"
	@echo "To run the GUI, type 'make gui'"
	@echo "To build package, type 'make build'"
	@echo "To upload tp PyPi, type 'make upload'"
	@echo "To clean up everything, type 'make clean'"
	@echo "-------------------------HELP-------------------------"

prepare:
	${PYTHON} -m venv .venv
	. .venv/bin/activate
	${PYTHON} -m pip install --upgrade pip
	${PIP} install -r requirements.txt
	${PIP} install pytest
	${PIP} install twine wheel

test:
	pytest

ui:
	pyuic5 StegLibrary/gui/gui.ui -o StegLibrary/gui/gui.py

gui: ui
	${PYTHON} -m StegLibrary gui

build: clean-build
	${PYTHON} setup.py sdist bdist_wheel

upload: build
	${PYTHON} -m twine upload dist/*

clean: clean-build clean-pyc clean-test

clean-build:
	rm -rf build/ dist/ *.egg-info

clean-pyc:
	find . -name "__pycache__" -exec rm -rf {} +

clean-test:
	rm -rf .pytest_cache