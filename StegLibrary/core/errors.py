# This file defines all errors raised by this application/library


class SteganographyError(BaseException):
    """
    This class inherits from the base BaseException class and all
    exceptions implemented in this library inherits from this class.
    """


class InputFileError(SteganographyError):
    """
    This class inherits from the base SteganographyError class.

    Raised when there is an I/O error when trying to read the input file.
    """


class OutputFileError(SteganographyError):
    """
    This class inherits from the base SteganographyError class.

    Raised when there is an I/O error when trying to write the output file.
    """


class InsufficientStorageError(SteganographyError):
    """
    This class inherits from the base SteganographyError class.

    Raised when there is insufficient storage to store all the data.
    """


class UnrecognisedHeaderError(SteganographyError):
    """
    This class inherits from the base SteganographyError class.

    Raised when failing to parse a header.
    """


class AuthenticationError(SteganographyError):
    """
    This class inherits from the base SteganographyError class.

    Raised when the provided authentication key is invalid.
    """
