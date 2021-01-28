# This script defines the Header class, whose functionality is to
# create and maintain the header of each steganograph.

import re
import hashlib
from StegLibrary.errors import HeaderError

class Header:
    """Provides for the preparation of the creation of steganographs."""

    # Signature for the header
    # Serve mainly as a decoration for now
    signature = "S{}T"

    # Padding character, used when header is too short
    # after writing all the required metadata
    padding_character = "-"

    # Separator is used to make regex easier
    separator = "?"

    # A default authentication key
    # To meet the API requirement
    default_key = "steganography"

    # Various types of length for the header
    metadata_length = 12
    key_hash_length = 4
    header_length = metadata_length + key_hash_length

    # Available density for steganograph
    available_density = (1, 2, 3)

    # Regex pattern of the header
    # TODO: Make a function to generate pattern on-demand
    # when the header structure changes
    pattern = r"^S(\d{1,6})\?([a-f\d]{2})\?([a-f\d]{4})T-*$"

    def __str__(self) -> str:
        """Returns the header."""
        return self.header

    def __dict__(self) -> dict:
        """Returns a dictionary of all metadata."""
        return {
            "data_length": self.data_length,
            "compression": self.compression,
            "density": self.density,
            "key": self.key,
        }

    def __repr__(self) -> str:
        """Same as __str__, returns the header."""
        return str(self)

    def __init__(self, data_length: int, compression: int, density: int, key: str) -> None:
        """
        Initilises a Header instance.

        * Positional arguments:

        data_length -- The (compressed) length (excluding header length) of the steganograph's data

        compression -- The level of data compression

        density -- The density level of the steganograph

        key_hash -- The hash of the validation key

        * Raises:

        HeaderError: Raised when the density requested is invalid
        """
        self.data_length = data_length
        self.compression = compression

        # Check if the requested density is allowed
        if density not in Header.available_density:
            raise HeaderError("InvalidDensity")
        self.density = density

        # Generate key hash with required length from key
        self.key_hash = hashlib.md5(key.encode()).hexdigest()[:Header.key_hash_length]

        # Generate header
        self.generate()

    def generate(self) -> None:
        """
        Generates a header created from data given during Header initialisation.

        There is no need to call this method, unless any metadata has been modified
        after initialisation.
        """
        # Create a flag from compression level and density level.
        # Bit 6 - 2: Compression level (0 (no compression) - 9)
        # Bit 1 - 0: Density level (1 - 3)
        flag = (self.compression << 2) + self.density

        # Mix flag in between key hash
        # Making it less obvious
        # Include a separator for easy parsing
        middle = int(self.key_hash_length / 2)
        mixer = self.key_hash[:middle] + Header.separator
        mixer += str(flag) + self.key_hash[middle:]

        # Put the mixer together with the data length
        # Include a padding as separator for easy parsing
        result_header = str(self.data_length) + Header.separator + mixer

        # Embed signature
        result_header = Header.signature.format(result_header)

        # Pad the resulting header to ensure correct length
        result_header += Header.padding_character * \
            (self.header_length - len(result_header))

        # Assign as a class attribute
        self.header = result_header

    @staticmethod
    def validate(header: str) -> bool:
        """
        Validates if header is valid.

        * Positional arguments:

        header -- Header to be validated
        """
        # Perform length check
        if len(header) != Header.header_length:
            return False

        # Perform pattern check
        if re.match(Header.pattern, header):
            return True

        return False

    @staticmethod
    def parse(header: str, key: str) -> dict:
        """
        Parses header into original metadata.

        * Positional arguments:

        header -- Header to be parsed

        key -- Validation key

        * Raises:

        HeaderError: Raised when header validation/parsing fails
        """
        result_dict = {
            "data_length": None,
            "compression": None,
            "density": None,
            "key_hash": None,
        }

        # Validate header
        if not Header.validate(header):
            raise HeaderError("InvalidFormat")

        # Generate Match object
        match = re.match(Header.pattern, header)

        # The first capturing group is the entire header, so ignore
        # Retrieve the second capturing group
        result_dict["data_length"] = int(match[1])

        # Retrieve the mixer (of flag and key hash) from the
        # third and fourth capturing groups
        mixer = match[2] + match[3]
        result_dict["key_hash"] = mixer[:2] + mixer[4:]
        flag = int(mixer[2:4])
        result_dict["density"] = flag & 0b11
        result_dict["compression"] = (flag - (flag & 0b11)) >> 2

        # Validate key hash
        key_hash = hashlib.md5(key.encode()).hexdigest()[:Header.key_hash_length]
        if key_hash != result_dict["key_hash"]:
            raise HeaderError("AuthError")

        # Return the resulting dictionary
        return result_dict
