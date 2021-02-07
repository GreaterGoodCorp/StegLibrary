# Builtin modules
from typing import Union
from io import RawIOBase, BufferedIOBase

# Internal modules
from StegLibrary.helper import err_imp

# Non-builtin modules
try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    err_imp("Pillow")
    exit(1)


def open_image(file: Union[RawIOBase, BufferedIOBase]):
    """Open an Image instance from the file object.

    ### Positional arguments

    - file (RawIOBase | BufferedIOBase)
        - A readable fileobject

    ### Returns

    A PIL.Image.Image instance of the image in file

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect types

    - IOError
        - Raised when file is unreadable

    - UnidentifiedImageError
        - Raised when the image cannot be retrieved from file
    """
    # Type checking
    if not isinstance(file, (RawIOBase, BufferedIOBase)):
        raise TypeError("File must be a binary fileobject")

    # Check if file is readable
    if not file.readable():
        raise IOError("File is unreadable")

    # Attempt to open and return Image
    try:
        return Image.open(file)
    except UnidentifiedImageError as e:
        raise e


def show_image(image: Image.Image) -> None:
    """Show this Image object on screen.

    ### Positional arguments

    - image (PIL.Image.Image)
        - The Image object to be shown

    ### Returns

    None

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect types
    """
    # 1. Type guarding
    try:
        # 2. Show the image using a builtin functions
        image.show("Demo")
        return
    except AttributeError:
        raise TypeError(f"Invalid image type (given {type(image)}")
