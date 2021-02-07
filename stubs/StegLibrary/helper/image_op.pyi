from PIL import Image
from StegLibrary.helper import err_imp as err_imp
from io import BufferedIOBase, RawIOBase
from typing import Any, Union

def open_image(file: Union[RawIOBase, BufferedIOBase]) -> Any: ...
def show_image(image: Image.Image) -> None: ...
