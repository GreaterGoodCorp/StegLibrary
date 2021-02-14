# Builtin modules
from sys import argv

# Internal modules
from StegLibrary.core.main import steg

# Main entry point for module
if __name__ == "__main__":
    argv[0] = "StegLibrary"
    steg()
