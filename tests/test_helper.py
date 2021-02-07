# Internal modules
from StegLibrary.helper import err_imp
from StegLibrary.helper import bit_op as bp

# Non-builtin modules
try:
    from pytest import raises
except ImportError:
    err_imp("pytest")
    exit(1)


def test_is_bit_set():
    # Assert 1: 0, 1
    assert not bp.is_bit_set(0, 0)
    assert bp.is_bit_set(1, 0)

    # Assert 2: Big number (452345)
    assert not bp.is_bit_set(452345, 8)
    assert bp.is_bit_set(452345, 9)

    # Assert 3: Error handling
    with raises(TypeError):
        bp.is_bit_set("434", 0)
    with raises(TypeError):
        bp.is_bit_set(434, "0")


def test_set_bit():
    # Assert 1: 0, 1
    assert bp.set_bit(0, 0) == 1
    assert bp.set_bit(1, 0) == 1

    # Assert 2: Big number
    assert bp.set_bit(423, 4) == 439
    assert bp.set_bit(12321, 9) == 12833

    # Assert 3: Error handling
    with raises(TypeError):
        bp.set_bit("2345")


def test_unset_bit():
    # Assert 1: 0, 1
    assert bp.unset_bit(0, 0) == 0
    assert bp.unset_bit(1, 0) == 0

    # Assert 2: Big number
    assert bp.unset_bit(439, 4) == 423
    assert bp.unset_bit(12833, 9) == 12321

    # Assert 3: Error handling
    with raises(TypeError):
        bp.unset_bit("2345")


def test_bitstr_from_int():
    # Assert 1: 0, 1
    assert bp.bitstr_from_int(0) == "0"
    assert bp.bitstr_from_int(1) == "1"

    # Assert 2: Big number
    assert bp.bitstr_from_int(12321) == "11000000100001"

    # Assert 3: With not enough length
    with raises(ValueError):
        bp.bitstr_from_int(12321, 8)

    # Assert 4: With extra length
    assert bp.bitstr_from_int(565, 12) == "001000110101"

    # Assert 5: Error handling
    with raises(TypeError):
        bp.bitstr_from_int("12321", 18)
    with raises(TypeError):
        bp.bitstr_from_int(12321, "18")


def test_int_from_bitstr():
    # Assert 1: 0, 1
    assert bp.int_from_bit_str("0") == 0
    assert bp.int_from_bit_str("1") == 1

    # Assert 2: Big number
    assert bp.int_from_bit_str("11000000100001") == 12321

    # Assert 3: With extra 0
    assert bp.int_from_bit_str("00111") == 7

    # Assert 4: Invalid characters
    with raises(ValueError):
        bp.int_from_bit_str("12321")

    # Assert 5: Error handling
    with raises(TypeError):
        bp.int_from_bit_str(10101)
