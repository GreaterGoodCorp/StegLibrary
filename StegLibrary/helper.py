from StegLibrary import ANSIFormatter
import os

print = ANSIFormatter.extendedPrint
steg_absolute_path = os.path.abspath(os.path.dirname(__file__))

def create_abspath(*rel_path):
    return os.path.join(steg_absolute_path, *rel_path)

def check_abspath(abspath):
    return os.path.isabs(abspath)

def split_path(path):
    return os.path.split(path)

def err_imp(pkg_name):
    s = f"[Package] This package is not installed: {pkg_name}"
    return print(s, ansi=ANSIFormatter.Red)