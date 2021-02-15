# Use external virtual environment manager
include Makefile.venv
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2020.08.14/Makefile.venv"
	echo "5afbcf51a82f629cd65ff23185acde90ebe4dec889ef80bbdc12562fbd0b2611 *Makefile.fetched" \
		| shasum -a 256 --check - \
		&& mv Makefile.fetched Makefile.venv

# GUI building/executing
ui: venv
	pyuic5 StegLibrary/gui/gui.ui -o StegLibrary/gui/gui.py

gui: ui
	${VENV}/python3 -m StegLibrary gui

# Cleanup everything
clean:
	rm -rf build/ dist/ *.egg-info
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

# Project testing
test: ${VENV}/pytest
	pytest

# Upload project to PyPI
upload: clean ${VENV}/twine ${VENV}/wheel
	${VENV}/python3 setup.py sdist bdist_wheel
	${VENV}/python3 -m twine upload dist/*