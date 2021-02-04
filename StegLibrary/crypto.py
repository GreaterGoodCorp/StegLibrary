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
