# StegLibrary

## Status
| Name          | Status                                                                                                                    |
|---------------|---------------------------------------------------------------------------------------------------------------------------|
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

* Creating steganographs

```python
def write_steg(data_file: str, image_file: str, key: str, compression: int, density: int, output_file: str) -> bool:
    """Write a steganograph
       
    * Positional arguments:
    
    data_file -- Path to data file
       
    image_file -- Path to image file
       
    key -- Authentication key
       
    compression -- Compression level
       
    density -- Density level
       
    output_file -- Path to output file
       
    * Raises:
       
    ImageFileValidationError: Raised when image validation failed
       
    DataFileValidationError: Raised when data validation failed
       
    InsufficientStorageError: Raised when there is insufficient storage
       
    UnavailableFileError: Raised when the output file already exists
       
    * Returns:
       
    True if a stegnograph has been successfully created and written on disks
    """
```

* Extracting steganographs

```python
def extract_steg(steg_file: str, output_file: str, key: str, stdout: bool = False) -> bool:
    """
    Extracts data from steganograph.
    
    * Positional arguments:
    
    steg_file -- Path to steganograph
    
    output_file -- Path to output file
    
    key -- Authentication key
    
    stdout -- Send output to sys.stdout
    
    * Returns:
    
    True if the steganograph is extracted and written to disk successfully
    
    * Raises:
    
    HeaderError: Raised when the header of the stegnograph is invalid
    """
```

### Command-line application

The package is also designed to be invoked from the CLI. The interface is written using `Click`.

#### Windows

Usage: `python -m StegLibrary [OPTIONS] COMMAND [ARGS] ...`

Help message can be printed by running `python -m StegLibrary --help`
