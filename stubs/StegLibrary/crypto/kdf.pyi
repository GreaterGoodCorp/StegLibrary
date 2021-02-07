from StegLibrary.helper import err_imp as err_imp
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def create_kdf(salt: bytes) -> PBKDF2HMAC: ...
