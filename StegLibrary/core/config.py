# This file defines SteganographyConfig class, which is used to
# configure all operations of the Steganography Library.

# Builtin modules
from typing import List


class SteganographyConfig(object):
    available_compression: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    available_density: List[int] = [1, 2, 3]

    default_compression: int = 9
    default_density: int = 1
    default_auth_key: str = "bGs21Gt@31"

    flag_close_on_exit: bool = True
    flag_show_image_on_completion: bool = False
    flag_fopen_mode: bool = "rb"
