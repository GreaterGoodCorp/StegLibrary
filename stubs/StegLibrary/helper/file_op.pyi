from io import BufferedIOBase, RawIOBase
from typing import Union

def raw_open(filename: str, mode: str=...) -> Union[RawIOBase, BufferedIOBase]: ...
