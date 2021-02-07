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


def show_image(image: Image.Image) -> None:
    """Show this Image object on screen

    ### Positional arguments

    - image (PIL.Image.Image)
        - The Image object to be shown

    ### Returns

    None
    """
    # 1. Type guarding
    try:
        # 2. Show the image using a builtin functions
        image.show("Demo")
        return
    except AttributeError:
        raise TypeError(f"Invalid image type (given {type(image)}")
