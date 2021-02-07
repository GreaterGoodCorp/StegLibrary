# StegLibrary

## Status

| Name          | Status                                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------- |
| PyPI version  | [![PyPi version](https://pypip.in/v/StegLibrary/badge.png)](https://crate.io/packages/StegLibrary/)                       |
| PyPI download | [![PyPi download](https://pypip.in/d/StegLibrary/badge.png)](https://crate.io/packages/StegLibrary/)                      |
| Build status  | [![Build Status](https://travis-ci.com/MunchDev/StegLibrary.svg?branch=main)](https://travis-ci.com/MunchDev/StegLibrary) |

StegLibrary is a Python 3 library that implements and extending on the practice of
Steganography, making it more accessible to average users.

## Disclaimer

I created this project during my free time (as a secondary school student). The code is really imperfect, but it is a great way
for me to try out different development technique. Hence, if you are a serious developer looking for a steganography library,
please **do not use** this one, since there are a lot of production-ready projects out there. However, if you are a hobbyist
like me, please feel free to clone/install this project, explore and even contribute! Again, if you are using project seriously,
please stop reading, otherwise please go ahead and read this entire file.

## Installation

Before installation, please make sure `python3` (version >= 3.6) is installed on your machine.

### Windows

Via `pip` (production):

```
python -m pip install --upgrade pip
pip install StegLibrary
```

Via source (testing/development):

```
git clone https://github.com/MunchDev/StegLibrary
cd StegLibrary
pip install -r requirements.txt
```

### MacOS / Unix

Via `pip` (production):

```bash
python3 -m pip install --upgrade pip
pip3 install StegLibrary
```

Via source (testing/development):

```bash
git clone https://github.com/MunchDev/StegLibrary
cd StegLibrary
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

## Usage

### Package structure & documentation

Once installed, the package can be imported with the name `StegLibrary`:

```python
import StegLibrary
```

The two available functions for creating and extracting steganographs are as follow:

- Creating steganographs

```python
def write_steg(
    input_file: Union[RawIOBase, BufferedIOBase],
    image_file: Image.Image,
    output_file: Union[RawIOBase, BufferedIOBase],
    *,
    auth_key: str = cfg.default_auth_key,
    compression: int = cfg.default_compression,
    density: int = cfg.default_density,
    close_on_exit: bool = cfg.flag_close_on_exit,
    show_image_on_completion: bool = cfg.flag_show_image_on_completion,
) -> bool:
    """Performs steaganography on input file and write data to image file.

    ### Positional arguments

    - input_file (RawIOBase | BufferedIOBase)
        - A readable file-like object of the input file

    - image_file (PIL.Image.Image)
        - An opened image object

    - output_file (RawIOBase | BufferedIOBase)
        - A writable file-like object of the output file

    ### Keyword arguments

    - auth_key (str) (default = cfg.default_auth_key)
        - The authentication key

    - compression (int) (default = cfg.default_compression)
        - The compression level

    - density (int) (default = cfg.default_density)
        - The data density

    - close_on_exit (bool) (default = cfg.flag_close_on_exit)
        - Whether to close the file objects on exit

    - show_image_on_completion (bool)
    (default = cfg.flag_show_image_on_completion)
        - Whether to show image on completion

    ### Return values

    True if the operation is successful, otherwise False

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - InputFileError
        - Raised when there is an I/O error when trying to read
        the input file

    - OutputFileError
        - Raised when there is an I/O error when trying to write
        the output file

    - InsufficientStorageError
        - Raised when the input file contains more data than
        the maximum storage
    """
```

- Extracting steganographs

```python
def extract_steg(
    input_file: Union[RawIOBase, BufferedIOBase],
    output_file: List[Union[RawIOBase, BufferedIOBase, TextIOBase]],
    *,
    auth_key: str = cfg.default_auth_key,
    close_on_exit: bool = cfg.flag_close_on_exit,
) -> bool:
    """Extract steaganography on input file and write data to output file.

    ### Positional arguments

    - input_file (RawIOBase | BufferedIOBase)
        - A readable file-like object of the input file

    - output_file (List[RawIOBase | BufferedIOBase | TextIOBase])
        - A list of writable file-like object(s) of the output file
        - NOTE: If sys.stdout (or any TextIOBase) is given, output
        will only be written if binary data can be decoded into string.

    ### Keyword arguments

    - auth_key (str) (default = cfg.default_auth_key)
        - The authentication key

    - close_on_exit (bool) (default = Config.flag_close_on_exit)
        - Whether to close the file objects on exit

    ### Return values

    True if the operation is successful, otherwise False

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - InputFileError
        - Raised when there is an I/O error when trying to read
        the input file

    - OutputFileError
        - Raised when there is an I/O error when trying to write
        the output file

    - UnrecognisedHeaderError
        - Raised when failing to parse a header

    - AuthenticationError
        - Raised when the provided authentication key is invalid
    """
```

### Command-line application

The package is also designed to be invoked from the CLI. The interface is written using `Click`.

Usage: `python -m StegLibrary [OPTIONS] COMMAND [ARGS] ...`

Help message can be printed by running `python -m StegLibrary --help`
