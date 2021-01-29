import pytest
import subprocess
import os

from StegLibrary.steglib import *
from StegLibrary.errors import *

tests_path = os.path.abspath(os.path.dirname(__name__))
tests_path = os.path.join(tests_path, "tests")
sample_txt_path = os.path.join(tests_path, "sample.txt")
sample_png_path = os.path.join(tests_path, "sample.png")
sample_jpg_path = os.path.join(tests_path, "sample.jpg")
sample_dir_path = os.path.join(tests_path, "sample_dir")
sample_non_path = os.path.join(tests_path, "sample.non")
sample_nor_path = os.path.join(tests_path, "sample.nor")

sample_bin_data = b"asdawerqe11231c2312ecSDCq12ec12ec"


@pytest.fixture(autouse=True)
def setup():
    subprocess.Popen("chmod 000 tests/sample.nor".split(" "))
    yield
    subprocess.Popen("chmod 444 tests/sample.nor".split(" "))


def test_image_file_validator():
    assert validate_image_file(sample_png_path)

    with pytest.raises(ImageFileValidationError):
        validate_image_file(sample_jpg_path)

    with pytest.raises(ImageFileValidationError):
        validate_image_file(sample_txt_path)

    with pytest.raises(ImageFileValidationError):
        validate_image_file(sample_dir_path)

    with pytest.raises(ImageFileValidationError):
        validate_image_file(sample_non_path)

    with pytest.raises(TypeError):
        validate_image_file(123)

    with pytest.raises(RelativePathError):
        validate_image_file(os.path.join("tests", "sample.png"))


def test_data_file_validator():
    assert validate_data_file(sample_png_path)
    assert validate_data_file(sample_jpg_path)
    assert validate_data_file(sample_txt_path)

    with pytest.raises(DataFileValidationError):
        validate_data_file(sample_dir_path)

    with pytest.raises(DataFileValidationError):
        validate_data_file(sample_non_path)

    with pytest.raises(TypeError):
        validate_data_file(123)

    with pytest.raises(RelativePathError):
        validate_data_file(os.path.join("tests", "sample.png"))


def test_preprocess_data_file():
    assert isinstance(preprocess_data_file(sample_png_path), bytes)
    assert isinstance(preprocess_data_file(sample_jpg_path), bytes)
    assert isinstance(preprocess_data_file(sample_txt_path), bytes)

    with pytest.raises(DataFileValidationError):
        preprocess_data_file(sample_nor_path)

    with pytest.raises(TypeError):
        validate_data_file(123)

    with pytest.raises(RelativePathError):
        preprocess_data_file(os.path.join("tests", "sample.png"))


def test_retrieve_image():
    assert retrieve_image(sample_png_path)

    with pytest.raises(ImageFileValidationError):
        retrieve_image(sample_jpg_path)

    with pytest.raises(ImageFileValidationError):
        retrieve_image(sample_txt_path)

    with pytest.raises(ImageFileValidationError):
        retrieve_image(sample_dir_path)

    with pytest.raises(ImageFileValidationError):
        retrieve_image(sample_non_path)

    with pytest.raises(TypeError):
        retrieve_image(123)

    with pytest.raises(RelativePathError):
        retrieve_image(os.path.join("tests", "sample.png"))


def test_check_file_availability():
    assert not check_file_availability(sample_jpg_path)
    assert check_file_availability(sample_non_path)

    with pytest.raises(TypeError):
        check_file_availability(123)

    with pytest.raises(RelativePathError):
        check_file_availability(os.path.join("tests", "sample.png"))

def test_write_output_data(tmpdir):
    assert write_output_data(sample_bin_data, os.path.join(tmpdir, "a"))

    with pytest.raises(TypeError):
        write_output_data(sample_dir_path, os.path.join(tmpdir, "b"))

    with pytest.raises(UnavailableFileError):
        write_output_data(sample_bin_data, os.path.join(tmpdir, "a"))