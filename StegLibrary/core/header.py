# This script defines the Header class, whose functionality is to
# create and maintain the header of each steganograph.

# Builtin modules
from re import compile

# Internal modules
from StegLibrary.core import SteganographyConfig as Config
from StegLibrary.core.errors import UnrecognisedHeaderError


class Header:
    """Provides for the preparation of the creation of steganographs."""

    # Padding character, used when header is too short
    # after writing all the required metadata
    padding_character = "-"

    # Separator is used to make regex easier
    separator = "?"

    # Various types of length for the header
    maximum_data_length = 8
    maximum_flag_length = 3
    salt_length = 24
    separator_length = 2
    header_length = maximum_data_length + \
        maximum_flag_length + salt_length + separator_length

    # Regex pattern of the header
    # data_length?flag?salt
    pattern = r"(\d{1,8})\?(\d{1,3})\?"
    hash_pattern = r"((?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==" + \
        r"|[A-Za-z0-9+/]{3}=)?)"
    pattern = compile(f"^{pattern + hash_pattern}$")

    def __str__(self) -> str:
        """Returns the header."""
        return self.header

    def __dict__(self) -> dict:
        """Returns a dictionary of all metadata."""
        return {
            "data_length": self.data_length,
            "compression": self.compression,
            "density": self.density,
            "salt": self.salt,
        }

    def __repr__(self) -> str:
        """Same as __str__, returns the header."""
        return str(self)

    def __init__(self, data_length: int, compression: int, density: int,
                 salt: str) -> None:
        self.data_length = data_length
        self.compression = compression
        self.density = density
        self.salt = salt

        self.generate()

    def generate(self) -> None:
        """
        Generates a header created from data given during
        Header initialisation.

        There is no need to call this method, unless any metadata has been
        modified after initialisation.
        """
        # Create a flag from compression level and density level.
        # Bit 6 - 2: Compression level (0 (no compression) - 9)
        # Bit 1 - 0: Density level (1 - 3)
        flag = (self.compression << 2) + self.density

        result_header = Header.separator.join(
            (str(self.data_length), str(flag), self.salt))

        assert Header.pattern.match(result_header)

        # Assign as a class attribute
        self.header = result_header


def build_header(
    *,
    data_length: int,
    compression: int = Config.default_compression,
    density: int = Config.default_density,
    salt: str,
) -> Header:
    """Builds the steganograph header with given data.

    ### Positional arguments

    - data_length (int)
        - The length of the steganograph (excluding the header)

    - compression (int) (default = Config.default_compression)
        - The compression level

    - density (int) (default = Config.default_density)
        - The data density

    - salt (str)
        - The 24-character salt string

    ### Returns

    A Header object containing all the data given
    """

    # Initialise the Header instance
    header = Header(
        data_length=data_length,
        compression=compression,
        density=density,
        salt=salt,
    )

    return header.header


def validate_header(b: bytes) -> bool:
    """Check if the bytes string contains valid Header.

    ### Positional arguments

    - b (bytes)
        - The bytes string to check

    ### Returns

    True if a Header is present, otherwise False

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types
    """
    # Type checking
    if not isinstance(b, bytes):
        raise TypeError(f"Must be a bytes string (given {type(b)})")

    # Try to decode into string
    try:
        s = str(b, "utf-8")
        return True if Header.pattern.match(s) else False
    except UnicodeDecodeError:
        return False


def parse_header(b: bytes) -> Header:
    """Parse a bytes string into a Header object.

    ### Postional arguments

    - b (bytes)
        - The bytes string to parse

    ### Returns

    A Header object from the bytes string

    ### Raises

    - TypeError
        - Raised when the parametres given are in incorrect types

    - UnrecognisedHeaderError
        - Raised when failing to parse a header.
    """
    # Type checking
    if not isinstance(b, bytes):
        raise TypeError(f"Must be a bytes string (given {type(b)})")

    # Validate header first
    if not validate_header(b):
        raise UnrecognisedHeaderError("Invalid header!")

    # Generate Match object of the header
    # Decode bytes string to string first
    header_match = Header.pattern.match(str(b, "utf-8"))

    # Extract data from capturing groups
    # Ignore first capturing groups
    # 1. Data length
    hdr_data_length = int(header_match[1])
    # 2. Setting flag
    hdr_flag = int(header_match[2])
    # 3. Salt
    hdr_salt = header_match[3]

    # Process flag
    hdr_density = hdr_flag & 0b11
    hdr_compression = (hdr_flag - hdr_density) >> 2

    # Build and return a Header object
    return build_header(
        data_length=hdr_data_length,
        compression=hdr_compression,
        density=hdr_density,
        salt=hdr_salt
    )
