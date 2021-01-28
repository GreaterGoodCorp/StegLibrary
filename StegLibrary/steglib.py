# This script implements the second version of steganography, which now includes
# an option to increase data density (using the two least significant bits) and
# an option to enable password verification.

# Builtins
import bz2
import base64
import imghdr
from os import path

import PIL

from StegLibrary import Header
from StegLibrary.errors import *
from StegLibrary.helper import err_imp

# Extra
try:
    from PIL import Image
except ImportError:
    err_imp("Pillow")
    exit(1)


def validate_image_file(image_file: str):
    """
    Validates image file by checking its availability and type.

    * Positional arguments:

    image_file (str) -- Path to image file

    * Returns:

    True if validation has run and succeeded

    * Raises:

    ImageFileValidationError: Raised when any validation step fails
    """
    # Make sure the path to image file exist, and it must be a file
    if not path.isfile(image_file):
        # If file does not exist, raise exception
        raise ImageFileValidationError("FileNotFound")
    # Make sure the image is in Portable Network Graphics (PNG) format
    # by checking the magic header (use of a builtin library)
    if imghdr.what != "png":
        # If file is not a PNG file
        # e.g return value is None for non-images
        # or the type of image
        raise ImageFileValidationError("NotImageFile")

    # Return True as a signal that the validation has been run and succeeded
    return True


def validate_data_file(data_file: str):
    """
    Validates data file by checking its availability.

    * Positional arguments:

    data_file -- Path to data file

    * Returns:

    True if validation has run and succeeded

    * Raises:

    DataFileValidationError: Raised when any validation step fails
    """
    # Make sure the path to data file exist, and it must be a file
    if not path.isfile(data_file):
        raise DataFileValidationError("FileNotFound")

    # Return True as a signal that the validation has been run and succeeded
    return True


def preprocess_data_file(data_file: str):
    # Perform validation again
    # just in case when the validation is not called
    validate_data_file(data_file)

    # Perform read operation on data file
    # Read in binary mod (rb) in order to correctly parse
    # binary data
    data = None
    try:
        # Attempt to perform operation
        with open(data_file, "rb") as file:
            data = file.read()
    except OSError as e:
        # If failed, wrap the original error inside custom error
        # for compatibility
        raise DataFileValidationError("IO", e)

    # Perform data validation
    if data == None or len(data) == 0:
        # If data is empty, raise error
        raise DataFileValidationError("EmptyFile")

    # Return data if all checks are good to go
    return data


def retrieve_image(image_file: str):
    """
    Retrieves the image from image file.

    Positional arguments:

    image_file -- Path to image file

    Returns:

    PIL.Image object of the image file

    Raises:

    ImageFileValidationError: Raised when any validation step fails
    """
    # Perform validation again
    # just in case when the validation is not called
    validate_image_file(image_file)

    # Attempt to read image data
    image = None
    try:
        image = Image.open(image_file)
    except PIL.UnidentifiedImageError as e:
        # If failed, wrap the original error inside custom error
        # for compatibility
        raise ImageFileValidationError("IO", e)

    # Perform image data validation
    if image == None:
        raise ImageFileValidationError("EmptyFile")

    # If image is successfully read then return
    return image


def write_steg(data_file: str, image_file: str, key: str, compression: int, density: int, output_file: str):
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

    * Returns:

    True if a stegnograph has been successfully created and written on disks

    """

    # Validate the (path to) image file and data file
    validate_image_file(image_file)
    validate_data_file(data_file)

    # Pre-process data file and read data
    data = preprocess_data_file(data_file)

    # Compress data (if needed)
    if compression > 0:
        data = str(base64.b64encode(bz2.compress(data, compression)), "utf-8")
    else:
        data = str(data, "utf-8")

    # Create header and append header
    header = Header(len(data), compression, density, key).header
    data = header + data

    # Serialise data
    data = bytes(data, "utf-8")

    # Read and retrieve image data
    image = retrieve_image(image_file)
    pix = image.load()
    x_dim, y_dim = image.size

    # Check if the image has enough room to store data
    no_of_pixel = x_dim * y_dim
    no_of_rgb = no_of_pixel * 3
    no_of_storable_bit = no_of_rgb * compression
    no_of_stored_bit = len(data) * 8
    if no_of_storable_bit < no_of_stored_bit:
        raise InsufficientStorageError()

    # Start writing steganograph
    x, y, count, bit_loc = 0, 0, 0, density
    current_pix = list(pix[0, 0])

    # Firstly, iterate through all the bytes to be written
    for byte in data:
        # Secondly, iterate through all the bits of the given byte
        for i in range(8):
            # Thirdly, check if the bit is set
            # If bit is set
            if byte & (1 << (7 - i)):
                # Check if the bit at the current location in the image is set
                # If unset then set it, otherwise unchange
                if not current_pix[count] & (1 << bit_loc):
                    current_pix[count] += 1 << bit_loc
            # If bit is unset
            else:
                # Check if the bit at the current location in the image is set
                # If set then unset it, otherwise unchange
                if current_pix[count] & (1 << bit_loc):
                    current_pix[count] -= 1 << bit_loc

            # Move to the next bit
            bit_loc -= 1
            # If reached the final bit
            if bit_loc == -1:
                # Move to the next RGB
                count += 1
                bit_loc = density
                # If reached the last RGB
                if count == 3:
                    # Save pixel and move to the next pixel
                    pix[x, y] = tuple(current_pix)
                    count = 0
                    y += 1
                    if y == y_dim:
                        y = 0
                        x += 1
                    current_pix = list(pix[x, y])

    # Save as PNG
    image.save(output_file)
    return 0


def extract_steg(steg_file, output_file, key, **kwargs):
    """Extracts data from steganograph.

    Args:

        steg_file -- Path to steganograph

        output_file -- Path to output file

        key -- Authentication key
    """
    # Load the steganograph
    im = Image.open(steg_file)
    pix = im.load()
    x_dim, y_dim = im.size
    x, y, count = 0, 0, 0
    result_data = b""

    density = 1
    bit_loc = density
    # Since the density is unknown, check all density
    # Attempt to retrieve the header
    while density in Header.available_density:
        bit_loc = density
        while len(result_data) < Header.header_length:
            byte = 0
            # Read every single bit
            # Mechanism is the same as the writing
            for i in range(8):
                # If bit is set, set the corressponding bit of 'byte'
                if pix[x, y][count] & (1 << bit_loc):
                    byte += (1 << (7 - i))
                bit_loc -= 1
                # If all readable bits are consumed
                if bit_loc == -1:
                    # Move to the next RGB
                    count += 1
                    bit_loc = density
                    # If all RGB are consume
                    if count == 3:
                        # Move to the next byte
                        count = 0
                        y += 1
                        if y == y_dim:
                            y = 0
                            x += 1
            # Convert the single byte to bytes
            result_data += byte.to_bytes(1, "big")
        # If header is invalid
        try:
            str(result_data, "utf-8")
        except:
            # Switch to the next possible density
            # Reset all values to original
            density += 1
            result_data = b""
            x, y, count = 0, 0, 0
        # If header is valid then stop
        else:
            break

    # If density is unavailable
    # i.e Not a valid header
    if density not in Header.available_density:
        # Raise error that the steganograph is invalid
        raise ValueError("Invalid steganograph")

    # Retrieve data from header
    header_metadata = Header.parse(str(result_data, "utf-8"), key)

    # Attempt to read the remaining data
    # Mechanism is same as above
    while len(result_data) < header_metadata["data_length"] + Header.header_length:
        byte = 0
        for i in range(8):
            if pix[x, y][count] & (1 << bit_loc):
                byte += (1 << (7 - i))
            bit_loc -= 1
            if bit_loc == -1:
                count += 1
                bit_loc = density
                if count == 3:
                    count = 0
                    y += 1
                    if y == y_dim:
                        y = 0
                        x += 1
        result_data += byte.to_bytes(1, "big")

    # Turn to string to strip header later
    result_data = str(result_data, "utf-8")

    # Strip header
    result_data = result_data[Header.header_length:]

    # If compressed, decompress
    if header_metadata["compression"] > 0:
        result_data = result_data[:result_data.find("=", -2)] + "=="
        result_data = bz2.decompress(
            base64.b64decode(bytes(result_data, "utf-8")))
    else:
        result_data = bytes(result_data, "utf-8")

    # Check if stdout is enabled then write
    if kwargs.get("std", None) == "stdout":
        print(str(result_data, "utf-8"))

    # Write data to output file
    with open(output_file, "wb") as f:
        f.write(result_data)

    return 0
