import pytest
from initial_solution import calculate_time, InsufficientArgsError, OutOfRangeError


def test_int_type_validation():
    with pytest.raises(TypeError):
        calculate_time([1, 2, 3], 'Not an int')


def test_list_type_validation():
    with pytest.raises(TypeError):
        calculate_time("Not a list", 1)


def test_bottles_list_types():
    with pytest.raises(TypeError):
        calculate_time([1, 'not int', 2, 3], 1)


def test_taps_in_range1():
    with pytest.raises(InsufficientArgsError):
        calculate_time([1, 2, 3], 0)


def test_taps_in_range2():
    with pytest.raises(InsufficientArgsError):
        calculate_time([1, 2, 3], -5)


def test_bottles_in_range1():
    with pytest.raises(InsufficientArgsError):
        calculate_time([], 2)


def test_bottles_in_range2():
    with pytest.raises(OutOfRangeError):
        calculate_time([100, -20, 200], 2)


def test_bottles_in_range3():
    with pytest.raises(OutOfRangeError):
        calculate_time([100, 0, 200], 2)
