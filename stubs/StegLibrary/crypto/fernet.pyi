from StegLibrary.helper import err_imp as err_imp
from cryptography.fernet import Fernet

def build_fernet(key: bytes) -> Fernet: ...
