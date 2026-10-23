import pytest
from app import calculate_discount, validate_task_title

def test_calculate_discount_standard():
    assert calculate_discount(100, 20) == 80.0
    assert calculate_discount(250, 10) == 225.0

def test_calculate_discount_boundary():
    assert calculate_discount(100, 0) == 100.0
    assert calculate_discount(100, 100) == 0.0

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(-50, 10)
    with pytest.raises(ValueError):
        calculate_discount(100, 120)

def test_validate_task_title():
    assert validate_task_title("Buy groceries") is True
    assert validate_task_title("   ") is False
    assert validate_task_title("") is False
    assert validate_task_title("a" * 101) is False