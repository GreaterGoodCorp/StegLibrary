from io import RawIOBase, BufferedIOBase
from typing import Union
from os import path

from StegLibrary.core import SteganographyConfig as Config


def raw_open(
    filename: str,
    mode: str = Config.flag_fopen_mode,
) -> Union[RawIOBase, BufferedIOBase]:
    """Opens a file and return its file object.

    ### Positional arguments

    - filename (str)
        - Absolute path to file

    - mode (str) (default = Config.flag_fopen_mode)
        - The mode to open the file (should be left default)

    ### Returns

    A RawIOBase or a BufferedIOBase file object of the file given

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - IOError
        - Raised when an I/O operation fails
    """
    # Type checking
    if not isinstance(filename, str):
        raise TypeError(f"Path to file must be string (given {type(filename)}")
    if not isinstance(mode, str):
        raise TypeError(f"Mode must be string (given {type(filename)}")

    # Check if path is absolute
    if not path.isabs(filename):
        raise IOError("Path must be absolute")

    # Attempt to open and return the file
    try:
        return open(filename, mode)
    except IOError:
        raise IOError("Unable to open file: " + filename)
