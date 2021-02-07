from PIL import Image
from StegLibrary.core.errors import AuthenticationError as AuthenticationError, InputFileError as InputFileError, InsufficientStorageError as InsufficientStorageError, OutputFileError as OutputFileError, UnrecognisedHeaderError as UnrecognisedHeaderError
from StegLibrary.core.header import Header as Header, build_header as build_header, parse_header as parse_header
from StegLibrary.crypto import InvalidToken as InvalidToken, build_fernet as build_fernet, create_kdf as create_kdf, extract_raw_salt as extract_raw_salt, make_salt as make_salt
from StegLibrary.helper import err_imp as err_imp, is_bit_set as is_bit_set, set_bit as set_bit, show_image as show_image, unset_bit as unset_bit
from io import BufferedIOBase, RawIOBase, TextIOBase
from typing import List, Union

def write_steg(input_file: Union[RawIOBase, BufferedIOBase], image_file: Image.Image, output_file: Union[RawIOBase, BufferedIOBase], *, auth_key: str=..., compression: int=..., density: int=..., close_on_exit: bool=..., show_image_on_completion: bool=...) -> bool: ...
def extract_header(image: Image.Image) -> Header: ...
def extract_steg(input_file: Union[RawIOBase, BufferedIOBase], output_file: List[Union[RawIOBase, BufferedIOBase, TextIOBase]], *, auth_key: str=..., close_on_exit: bool=...) -> bool: ...
