# This script implements the second version of steganography, which now includes
# an option to increase data density (using the two least significant bits) and
# an option to enable password verification.

# Builtin modules
import io
import bz2
import base64
from os import path
from typing import Union

# Internal modules
from StegLibrary import cfg
from StegLibrary.crypto import make_salt, create_kdf, build_fernet
from StegLibrary.header import build_header
from StegLibrary.errors import *
from StegLibrary.helper import err_imp, is_bit_set, set_bit, show_image, unset_bit

# Non-builtin modules
try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    err_imp("Pillow")
    exit(1)


def write_steg(
    input_file: Union[io.RawIOBase, io.BufferedIOBase],
    image_file: Image.Image,
    output_file: Union[io.RawIOBase, io.BufferedIOBase],
    *,
    auth_key: str = cfg.default_auth_key,
    compression: int = cfg.default_compression,
    density: int = cfg.default_density,
    close_on_exit: bool = cfg.flag_close_on_exit,
    show_image_on_completion: bool = cfg.flag_show_image_on_completion,
) -> bool:
    """Performs steaganography on input file and write data to image file.

    ### Positional arguments

    - input_file (io.RawIOBase | io.BufferedIOBase)
        - A readable file-like object of the input file

    - image_file (PIL.Image.Image)
        - An opened image object

    - output_file (io.RawIOBase | io.BufferedIOBase)
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

    ### Return values

    True if the operation is successful, otherwise False

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - InputFileError
        - Raised when there is an I/O error when trying to read the input file

    - OutputFileError
        - Raised when there is an I/O error when trying to write the output file

    - InsufficientStorageError
        - Raised when the input file contains more data than the maximum storage
    """

    # Validate input file
    # 1. Type guard
    try:
        # 2. Check that the file can be read.
        if not input_file.readable():
            raise InputFileError("Input file is not readable!")
    except AttributeError:
        raise InputFileError("Input file must be a readable file-like object!")

    # Read data from input file
    # 1. Return to the starting index first, to avoid exhaustion.
    input_file.seek(0)
    # 2. Read data to memory
    # This can return a bytes object or a NoneType.
    data = input_file.read()
    # 3. Check that the data is not None
    if isinstance(data, None):
        raise InputFileError("Input file is not readable!")
    # 4. Check that the data is non-empty
    if len(data) == 0:
        raise InputFileError("Input file is empty or exhausted!")

    # Compress data
    # 1. Type checking
    if not isinstance(compression, int):
        raise TypeError(
            f"Compression must be an integer (given {type(compression)} instead)"
        )
    # 2. Check if compression level is valid by compare with configuration
    if compression not in cfg.available_compression:
        raise ValueError("Compression level not defined!")
    # 3. Start compression, unless disabled by the caller
    if compression > 0:
        # Compress using the builtin bzip2 library
        data = bz2.compress(data, compresslevel=compression)

    # Encrypt data
    # 1. Type checking
    if not isinstance(auth_key, str):
        raise TypeError(
            f"Authentication key must be a string (given {type(auth_key)} instead)"
        )
    # 2. Make salt
    salt, salt_str = make_salt()
    # 3. Make KDF
    kdf = create_kdf(salt)
    # 4. Derive key from auth_key
    # Authentication key will be encoded first to pass to KDF.
    key = kdf.derive(auth_key.encode())
    # 5. Build Fernet
    # Fernet is a simple, symmetric (secret key) authenticated cryptography.
    # a.k.a, it is secure and easy to implement.
    fn = build_fernet(key)
    # 6. Start encryption
    # Data will be passed through Fernet
    data = fn.encrypt(data)

    # Craft the finished data
    # 1. Build a header for the steganograph
    header = build_header(
        data_length=len(data),
        compression=compression,
        density=density,
        salt=salt_str,
    )
    # 2. Serialise header and prepend data with header
    data = bytes(header, "utf-8") + data

    # Retrieve access to pixel data
    # 1. Type guarding
    try:
        # 2. Load PixelAccess
        pix = image_file.load()
    except AttributeError:
        raise TypeError(
            f"Image file must be a PIL.Image.Image (given {type(image_file)})")

    # Retrieve metadata of image file
    x_dim, y_dim = image_file.size

    # Check if the image has enough room to store data
    # 1. Find the number of writable pixels
    no_of_pixel = x_dim * y_dim
    # 2. Find the number of colour codes by multyplying by 3
    # since each pixel contains 3 integers
    no_of_rgb = no_of_pixel * 3
    # 3. Depending on the density, find the maximum number
    # of bits can be stored
    no_of_storable_bit = no_of_rgb * density
    # 4. Find the number of bits to be stored by
    # multiplying by 8 (1 byte contains 8 bit)
    no_of_stored_bit = len(data) * 8

    # Make sure there are enough space to store all bits
    if no_of_storable_bit < no_of_stored_bit:
        # If there are not enough, raise error
        raise InsufficientStorageError("Data is too big to be stored!")

    # Start writing steganograph
    # Declare usable variables as pointer to bit being written
    x, y, count, bit_loc = 0, 0, 0, density
    # Declare a local variable for pixel to reduce look-up time
    current_pix = list(pix[0, 0])

    # Firstly, iterate through all the bytes to be written
    for byte in data:
        # Secondly, iterate through all the bits of the given byte
        for i in range(8):
            # Thirdly, check if the bit is set
            # If bit is set
            if is_bit_set(byte, i):
                # Check if the bit at the current location in the image is set
                # If unset then set it, otherwise unchange
                current_pix[count] = set_bit(current_pix[count], bit_loc)
            # If bit is unset
            else:
                # Check if the bit at the current location in the image is set
                # If set then unset it, otherwise unchange
                current_pix[count] = unset_bit(current_pix[count], bit_loc)

            # Move to the next bit
            # by decrementing index
            bit_loc -= 1
            # If reached the final bit
            if bit_loc == -1:
                # Move to the next integer
                # by incrementing the count
                count += 1
                # Reset density
                bit_loc = density
                # If reached the last RGB
                if count == 3:
                    # Save pixel
                    pix[x, y] = tuple(current_pix)
                    # Reset count
                    count = 0
                    y += 1
                    # If the entire row of pixel is written
                    if y == y_dim:
                        # Move on to the next row and reset
                        y = 0
                        x += 1
                    # Request new pixel to be written
                    current_pix = list(pix[x, y])

    # Save as PNG
    image_file.save(output_file, "png")

    # Check if image should be shown on completion
    if show_image_on_completion:
        show_image(image_file)

    # Check if close on exit flag is enabled
    if close_on_exit:
        # If enabled, close all file objects
        input_file.close()
        image_file.close()
        output_file.close()

    # At this step, operation is successful, so return True
    return True


def extract_steg(steg_file: str,
                 output_file: str,
                 key: str,
                 stdout: bool = False,
                 header_only: bool = False) -> bool:
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

    TypeError: Raised when the parametres are of incorrect types

    HeaderError: Raised when the header of the stegnograph is invalid

    """

    # Validate the steganograph
    validate_image_file(steg_file)

    # Check availability of output file
    # No output for validation, so just add a guard
    if not (header_only or check_file_availability(output_file)):
        # If file is already taken, raise error
        raise UnavailableFileError()

    # Retrieve image data
    image = retrieve_image(steg_file)

    # Load the steganograph and its metadata
    image = Image.open(steg_file)
    pix = image.load()
    y_dim = image.size[1]

    # Declare some local variables as the extraction starts
    x, y, count = 0, 0, 0
    result_data = b""
    density = 1
    bit_loc = density

    # Firstly, the header is retrieved by reading for its known length.
    # Since the density is unknown, check all density one by one.
    while density in Header.available_density:
        bit_loc = density
        while len(result_data) < Header.header_length:
            byte = 0
            # Read every single bit
            # Iterate through every single bit of the byte
            for i in range(8):
                # If bit is set, set the corressponding bit of 'byte'
                if pix[x, y][count] & (1 << bit_loc):
                    byte += (1 << (7 - i))
                # Move to the next bit by decrement bit index
                bit_loc -= 1
                # If all readable bits of the colour integer are consumed
                if bit_loc == -1:
                    # Move to the next RGB and reset the bit index
                    count += 1
                    bit_loc = density
                    # If the entire pixel is read
                    if count == 3:
                        # Move to the next pixel in the row and reset the count
                        count = 0
                        y += 1
                        # If the entire row of pixels is read
                        if y == y_dim:
                            # Move to the next row and reset row index
                            y = 0
                            x += 1
            # Convert the single byte (integer) to bytes
            # By design, the resulting data is strictly stored in 1 byte
            # and endianness does not matter since it is only 1 byte
            result_data += byte.to_bytes(1, "big")
        # If header is invalid
        # e.g wrong density
        try:
            # Invalid header has undecodable byte
            str(result_data, "utf-8")
        except:
            # Hence, switch to the next possible density
            # Reset all values to original
            density += 1
            result_data = b""
            x, y, count = 0, 0, 0
        # If header is valid then stop
        else:
            break

    # If density is unavailable
    # i.e Not a valid header -> Invalid steganograph
    if density not in Header.available_density:
        # Raise error that the steganograph is invalid
        raise HeaderError("InvalidFormat")

    # Retrieve data from header
    # Note, HeaderError will be raised if parsing is not done
    header_metadata = Header.parse(str(result_data, "utf-8"), key, header_only)

    # Return on completion of validation
    if header_only:
        return header_metadata

    # Attempt to read the remaining data
    # Continue with the result variable already containing the header
    # which will be stripped later
    while len(result_data
              ) < header_metadata["data_length"] + Header.header_length:
        byte = 0
        # Read every single bit
        # Iterate through every single bit of the byte
        for i in range(8):
            # If bit is set, set the corressponding bit of 'byte'
            if pix[x, y][count] & (1 << bit_loc):
                byte += (1 << (7 - i))
            # Move to the next bit by decrement bit index
            bit_loc -= 1
            # If all readable bits of the colour integer are consumed
            if bit_loc == -1:
                # Move to the next RGB and reset the bit index
                count += 1
                bit_loc = density
                # If the entire pixel is read
                if count == 3:
                    # Move to the next pixel in the row and reset the count
                    count = 0
                    y += 1
                    # If the entire row of pixels is read
                    if y == y_dim:
                        # Move to the next row and reset row index
                        y = 0
                        x += 1
        # Convert the single byte (integer) to bytes
        # By design, the resulting data is strictly stored in 1 byte
        # and endianness does not matter since it is only 1 byte
        result_data += byte.to_bytes(1, "big")

    # Strip header by slicing its known length
    result_data = result_data[Header.header_length:]

    # If compressed (as indicated by the header), decompress it
    if header_metadata["compression"] > 0:
        # NOTE: This is a temporary fix as mentioned in the issue
        # The last few bits are read improbably, hence the
        # base64 padding is wrong
        # This part removes the invalid padding and append
        # a valid one.

        # Find the index of padding
        padding_index = result_data.find(b"=", -2)

        # Remove the padding by slicing and add the new padding
        result_data = result_data[:padding_index] + b"=="

        # Base64-decode the data and decompress
        result_data = bz2.decompress(base64.b64decode(result_data))

    # Check if stdout is enabled then write to sys.stdout
    if stdout:
        try:
            # Try to print string
            print(str(result_data, "utf-8"))
        except:
            # However if not supported (e.g binary data)
            # then print raw binary data
            print(result_data)

    # Write data to output file
    write_output_data(result_data, output_file)

    return True
