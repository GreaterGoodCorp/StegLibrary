# Builtin modules
from base64 import b64encode, b64decode
from binascii import Error
from os import urandom
from typing import Tuple


def make_salt() -> Tuple[bytes, str]:
    """Makes a random salt for KDF.

    ### Returns

    - bytes
        - A 16-byte salt

    - str
        - A base64-encoded string representation of the salt
    """
    # Generate a cryptographically secure random bytes
    salt = urandom(16)

    # Return the salt with the base64 string
    return salt, str(b64encode(salt), "utf-8")

def extract_raw_salt(salt_str: str) -> bytes:
    """Extract raw salt from the given salt string.

    ### Positional arguments

    - salt_str (str)
        - A salt string

    ### Returns

    - bytes
        The salt from the salt string

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - ValueError
        - Raised when the parametres given are invalid
    """
    # Type checking
    if not isinstance(salt_str, str):
        raise TypeError(f"The salt must be a string (given {type(salt_str)})")

    # Length checking
    # A 16-byte salt when encoded produces a 24-character string
    if len(salt_str) != 24:
        raise ValueError("Invalid salt string")

    # Extract salt
    # 1. Decoding guard: shield against invalid salt string
    try:
        # Decode string from UTF-8 before passing on
        # Return the base64-decoded bytes
        return b64decode(bytes(salt_str, "utf-8"))
    except Error:
        # Missing padding, caused when the salt string is corrupted
        raise ValueError("Invalid salt string")