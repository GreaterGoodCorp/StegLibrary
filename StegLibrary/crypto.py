from base64 import b64encode, b64decode
from binascii import Error
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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


def create_kdf(salt: bytes) -> PBKDF2HMAC:
    """Builds a key derive function with the salt given.

    ### Keyword arguments

    - salt (bytes)
        - A random 16-byte salt (can be made from make_salt())

    ### Returns

    A PBKDF2HMAC object, with can be used to derive key from password

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types
    """
    # Type checking
    if not isinstance(salt, bytes):
        raise TypeError(f"The salt must be in bytes (given {type(salt)})")

    # Initialise and return a PBKDF2HMAC object
    return PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend(),
    )


def build_fernet(key: bytes) -> Fernet:
    """Build a Fernet object to encrypt or decrypt data from the key.

    ### Positional arguments

    - key (bytes)
        - A derived key (can be derived using the KDF from make_kd())

    ### Returns

    A Fernet object

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types
    """
    # Type checking
    if not isinstance(key, bytes):
        raise TypeError(f"The key must be in bytes (given {type(key)})")

    # Initialise and return a Fernet object
    return Fernet(key)

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