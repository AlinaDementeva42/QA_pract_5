import pytest
from calculator import add_numbers

# 1. Фикстура с параметризацией (подготовка данных)
@pytest.fixture(params=[
    (1, 2),
    (5, 5),
    (10, 20),
])
def positive_pairs(request):
    return request.param

@pytest.fixture(params=[
    (5, -3),
    (-1, -2, 10),
    (10, -5, -2, 1),
    (-10, -20, -30),
])
def mixed_numbers(request):
    return request.param

@pytest.fixture(params=[
    (0, 0, 0),
    (1, 0),
    (-5, 0, 5),
    (0, 0, 0, 0, 0)
])
def zero_sets(request):
    return request.param

# 2. Тесты
def test_add_positive(positive_pairs):
    result = add_numbers(*positive_pairs)
    expected = sum(positive_pairs)
    assert result == expected
    assert result > 0

def test_add_mixed(mixed_numbers):
    result = add_numbers(*mixed_numbers)
    expected = sum(mixed_numbers)
    assert result == expected

def test_add_with_zeros(zero_sets):
    result = add_numbers(*zero_sets)
    expected = sum(zero_sets)
    assert result == expected

    extended_set = zero_sets + (0,)
    assert add_numbers(*extended_set) == expected