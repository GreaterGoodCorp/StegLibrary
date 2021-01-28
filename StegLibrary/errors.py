# This file defines all errors raised by this application/library

class SteganographyError(Exception):
    """
    This class inherits from the base Exception class and all 
    exceptions implemented in this library inherits from this class.

    Raised when an exception occurs inside its subclasses.
    """

    def __init__(self, sub_class: bool = True, *args: object) -> None:
        super().__init__(*args)
        self.sub_class = args[0] if sub_class else None
        self.sub_msg = args[1] if sub_class else None

    def __str__(self) -> str:
        if self.sub_class:
            return f"Raised by {self.sub_class.__name__} with message: {self.sub_msg}"


class ImageFileValidationError(SteganographyError):
    """
    This class inherits from the base Steganography class.

    Raised when there is an error during the image file validation process.
    """
    all_errors = {
        "FileNotFound": "The image file specified is not found",
        "NotImageFile": "The file given is not an image file",
    }

    def __init__(self, error_type, *args: object) -> None:
        super().__init__(*args)
        if error_type not in ImageFileValidationError.all_errors:
            raise SteganographyError(
                True, ImageFileValidationError, "The specified error type is invalid")
        self.error_type = error_type

    def __str__(self) -> str:
        return ImageFileValidationError.all_errors[self.error_type]
