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
    if imghdr.what(image_file) != "png":
        # If file is not a PNG file
        # e.g return value is None for non-images
        # or the type of image
        raise ImageFileValidationError("NotImageFile")

    # Return True as a signal that the validation has been run and succeeded
    return True


def validate_data_file(data_file: str) -> bool:
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


def preprocess_data_file(data_file: str) -> bytes:
    """
    Pre-processes data file by reading and checking integrity.

    * Positional arguments:

    data_file -- Path to data file

    * Returns:

    Binary data (as bytes) of the data file

    * Raises:

    DataFileValidationError: Raised when data file is unreadable or corrupted
    """
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


def retrieve_image(image_file: str) -> Image:
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


def check_file_availability(file: str) -> bool:
    """
    Checks if file exists already.

    * Positional arguments:

    file -- Path to file to be checked

    * Returns:

    True if file does not exist, otherwise False
    """
    # Check if file is already exist
    if path.exists(file):
        return False
    return True


def write_output_data(data: bytes, output_file: str) -> bool:
    """
    Writes binary data to output file.

    * Positional arguments:

    data -- Binary data to be written

    output_file -- Path to output file

    * Returns:

    True if data is written succesfully to output file

    * Raises:

    UnavailableFileError: Raised when the destination file is unavailable

    OutputFileIOError: Raised when data cannot be written to file due to I/O error
    """
    # Check if output file is available
    if not check_file_availability(output_file):
        raise UnavailableFileError()

    # Attempt to write data to output file
    try:
        # Write in binary to write binary data
        with open(output_file, "wb") as file:
            file.write(data)
    except OSError as e:
        # Raise custom error with internal error as an argument
        # for easy debugging
        raise OutputFileIOError(e)

    # Return True as a signal that write operation succeeded
    return True


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

    # Validate the (path to) image file and data file
    validate_image_file(image_file)
    validate_data_file(data_file)

    # Check file availability
    if not check_file_availability(output_file):
        # If file is already taken, raise error
        raise UnavailableFileError()

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
    # First find the number of writable pixels
    no_of_pixel = x_dim * y_dim
    # Then, the number of colour codes by multyplying by 3
    # since each pixel contains 3 integers
    no_of_rgb = no_of_pixel * 3
    # Next, depending on the density, find the maximum number
    # of bits can be stored
    no_of_storable_bit = no_of_rgb * density
    # Finally, find the number of bits to be stored by
    # multiplying by 8 (1 byte contains 8 bit)
    no_of_stored_bit = len(data) * 8

    # Make sure there are enough space to store all bits
    if no_of_storable_bit < no_of_stored_bit:
        # If there are not enough, raise error
        raise InsufficientStorageError()

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
    image.save(output_file)
    return 0


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

    # Validate the steganograph
    validate_image_file(steg_file)

    # Check availability of output file
    if not check_file_availability(output_file):
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
        raise ValueError("Invalid steganograph")

    # Retrieve data from header
    # Note, HeaderError will be raised if parsing is not done
    header_metadata = Header.parse(str(result_data, "utf-8"), key)

    # Attempt to read the remaining data
    # Continue with the result variable already containing the header
    # which will be stripped later
    while len(result_data) < header_metadata["data_length"] + Header.header_length:
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
