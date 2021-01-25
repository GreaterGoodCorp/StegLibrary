# This script implements the second version of steganography, which now includes
# an option to increase data density (using the two least significant bits) and
# an option to enable password verification.

# Builtins
import hashlib
import bz2
import base64
import imghdr

from StegLibrary import Header, err_imp

# Extra
try:
    from PIL import Image
except ImportError:
    err_imp("Pillow")
    exit(1)


def write_steg(data_file: str, image_file: str, key: str, compression: int, density: int, output_file: str):
    """Write a steganograph

    Args:

        data_file (str): Path to data file

        image_file (str): Path to image file

        key (str): Authentication key

        compression (int): Compression level

        density (int): Density level

        output_file (str): Path to output file
    """
    # Check if the image is PNG.
    if imghdr.what(image_file) != "png":
        raise ValueError("The image provided must be PNG!")

    # Read the binary data
    with open(data_file, "rb") as f:
        data = f.read()

    # Calculate key hash
    key = hashlib.md5(key.encode()).hexdigest()[:Header.key_hash_length]

    # Compress data (if needed)
    if compression > 0:
        data = str(base64.b64encode(bz2.compress(data, compression)), "ascii")
    else:
        data = str(data, "ascii")

    # Create header and append header
    header = Header(len(data), compression, density, key).header
    data = header + data

    # Serialise data
    data = bytes(data, "ascii")

    # Retrieve metadata of the image
    im = Image.open(image_file)
    pix = im.load()
    x_dim, y_dim = im.size

    # Check if the image has enough room to store data
    no_of_pixel = x_dim * y_dim
    no_of_rgb = no_of_pixel * 3
    no_of_storable_bit = no_of_rgb * compression
    no_of_stored_bit = len(data) * 8
    if no_of_storable_bit < no_of_stored_bit:
        raise OverflowError(
            "The storage is not big enough to perform steganography!")

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
    im.save(output_file, "png")
    return 0


def extract_steg(steg_file, output_file, key):
    """Extracts data from steganograph.

    Args:

        steg_file (str): Path to steganograph

        output_file (str): Path to output file

        key (str): Authentication key
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
            str(result_data, "ascii")
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
    header_metadata = Header.parse(str(result_data, "ascii"))

    # Calculate key hash
    key_hash = hashlib.md5(key.encode()).hexdigest()[:Header.key_hash_length]

    # Authenticate
    if key_hash != header_metadata["key_hash"]:
        raise ValueError("Authentication key does not match!")

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
    result_data = str(result_data, "ascii")

    # Strip header
    result_data = result_data[Header.header_length:]

    # If compressed, decompress
    if header_metadata["compression"] > 0:
        result_data = bz2.decompress(
            base64.b64decode(bytes(result_data, "ascii")))
    else:
        result_data = bytes(result_data, "ascii")

    # Check if output is stdout, i.e. console output
    if output_file == "stdout":
        print(str(result_data, "ascii"))

    # Write data to output file
    with open(output_file, "wb") as f:
        f.write(result_data)

    return 0
