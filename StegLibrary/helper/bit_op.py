# Builtin modules
from typing import Optional
from itertools import count


def is_bit_set(i: int, pos: int) -> bool:
    """Checks if bit is set

    ### Positional arguments
    - i (int)
        - An integer to check
    - pos (int)
       - Position of the bit to check (indexed from the last significant bit)

    ### Returns
    True if bit is set, otherwise False

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect type
    """
    # Type checking
    if not (isinstance(i, int) and isinstance(pos, int)):
        raise TypeError(f"Must be an integer (given {type(i)} instead)")

    # Check bit by performing bitwise operations AND
    # Explanation:
    # Given an integer i = 10101010, to check if the fourth to last bit
    # (pos = 3) is set, AND it with number n = 00001000 = 2 ** pos. Since n
    # contains bit 0 everywhere except at the pos, the result of AND will be
    # 0000x000, with x is equal to 1 if the pos-th bit of i is set, 0
    # otherwise. If x is 1, the result will be a non-zero number, 0 otherwise.
    # Hence, the bit is set if the result is non-zero, unset otherwise
    return i & (1 << pos)


def set_bit(i: int, pos: int) -> int:
    """Sets a bit of an integer at the given index.

    ### Positional arguments
    - i (int)
        - An integer to set
    - pos (int)
        - Position of the bit to set (indexed from the last significant bit)

    ### Returns

    An integer, with the bit at the position set.

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect type
    """
    # Type checking
    if not (isinstance(i, int) and isinstance(pos, int)):
        raise TypeError(f"Must be an integer (given {type(i)} instead)")

    # Check if the bit is set
    if is_bit_set(i, pos):
        # If bit is already set, ignore and return
        return i
    else:
        # If bit is not set, set the bit by adding into it 1 << pos
        # or 2 ** pos. For example, given an integer i = 10011001, in
        # order to set bit at pos = 5, add n = 00100000 to i. After
        # this, the bit will be set (i = 10111001).
        return i + (1 << pos)


def unset_bit(i: int, pos: int) -> int:
    """Unsets a bit of an integer at the given index.

    ### Positional arguments
    - i (int)
        - An integer to unset
    - pos (int)
        - Position of the bit to unset (indexed from the last significant bit)

    ### Returns

    An integer, with the bit at the position unset.

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect type
    """
    # Type checking
    if not (isinstance(i, int) and isinstance(pos, int)):
        raise TypeError(f"Must be an integer (given {type(i)} instead)")

    # Check if the bit is unset
    if not is_bit_set(i, pos):
        # If bit is already set, ignore and return
        return i
    else:
        # If bit is not set, set the bit by adding into it 1 << pos
        # or 2 ** pos. For example, given an integer i = 10011001, in
        # order to set bit at pos = 5, subtract n = 00100000 to i.
        # After this, the bit will be set (i = 10111001).
        return i - (1 << pos)


def bitstr_from_int(
    i: int,
    length: Optional[int] = None
) -> str:
    """Returns binary representation of an integer

    ### Positional arguments

    - i (int)
        - An integer
    - length (int)
        - The length of binary representation

    ### Returns

    A string of binary representation of the integer

    ### Raises

    - TypeError
        - Raised when the parametres are of incorrect type

    - ValueError
        - Raised when length is less than the minimum length
        of the string
    """
    # Type checking
    if not isinstance(i, int):
        raise TypeError(f"i must be integer (given {type(i)})")
    if not (isinstance(length, int) or length is None):
        raise TypeError("length must be integer or None " +
                        f"(given {type(length)})")

    # Make default length
    # If length is None only
    for length in count():
        if (1 << length) - 1 >= i:
            break

    # Maximum value of n-bit integer is (1 << n) - 1 (when all bits are set)
    # So check the number i with (1 << length) - 1
    if i > (1 << length) - 1:
        raise ValueError("Length is less than the minimum length required")

    result_str = ""
    # This thing works by checking the bit at the location (using is_bit_set())
    # Then, prepend "1" or "0" as required.
    for loc in range(length):
        result_str = ("1" if is_bit_set(i, loc) else "0") + result_str

    return result_str

