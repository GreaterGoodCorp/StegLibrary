# Internal modules
from StegLibrary.helper import err_imp

# Non-builtin modules
try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    err_imp("cryptography")
    exit(1)

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
