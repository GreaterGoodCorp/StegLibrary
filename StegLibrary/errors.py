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
        "FileNotFound": "The image file specified is not found or is a directory.",
        "NotImageFile": "The file given is not an image file.",
        "EmptyFile": "The image file is unreadable or corrupted.",
        "IO": "The image file cannot be read or opened.",
    }

    def __init__(self, error_type, *args: object) -> None:
        super().__init__(*args)
        if error_type not in ImageFileValidationError.all_errors:
            raise SteganographyError(
                True, ImageFileValidationError, "The specified error type is invalid")
        self.error_type = error_type
        if error_type == "IO":
            if len(args) == 0:
                raise SteganographyError(
                    True, ImageFileValidationError, "Missing information")
        self.inner_error = args[0]

    def __str__(self) -> str:
        return ImageFileValidationError.all_errors[self.error_type]


class DataFileValidationError(SteganographyError):
    """
    This class inherits from the base Steganography class.

    Raised when there is an error during the data file validation process.
    """
    all_errors = {
        "FileNotFound": "The data file specified is not found or is a directory.",
        "EmptyFile": "The data file is empty or unreadable.",
        "IO": "The data file cannot be read or opened."
    }

    def __init__(self, error_type, *args: object) -> None:
        super().__init__(*args)
        if error_type not in DataFileValidationError.all_errors:
            raise SteganographyError(
                True, DataFileValidationError, "The specified error type is invalid")
        self.error_type = error_type
        if error_type == "IO":
            if len(args) == 0:
                raise SteganographyError(
                    True, DataFileValidationError, "Missing information")
        self.inner_error = args[0]

    def __str__(self) -> str:
        if self.error_type == "IO":
            return str(self.inner_error)
        else:
            return DataFileValidationError.all_errors[self.error_type]

class InsufficientStorageError(SteganographyError):
    """
    This class inherits from the base Steganography class.

    Raised when there is insufficient storage to store data in the image file.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "There is insufficient storage in image file."
