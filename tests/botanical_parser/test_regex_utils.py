"""
Tests for the regex_utils module.
"""
import re
import pytest
from src.botanical_parser.regex_utils import generate_attribute_regex, generate_numeric_regex


color_value_words = [
    "green", "red", "blue", "purple", "yellow", "orange", "pink", "white", "black", "brown", "gray", "purple"
]


def test_match_simple_value():
    """Test matching a simple value word."""
    pattern = generate_attribute_regex(value_words=color_value_words)
    regex = re.compile(f"^{pattern}$")
    
    # Simple value words
    assert regex.match("green")
    assert regex.match("red")
    assert regex.match("blue")
    assert regex.match("purple")


def test_match_with_qualifiers():
    """Test matching values with qualifiers."""
    pattern = generate_attribute_regex(value_words=color_value_words)
    regex = re.compile(f"^{pattern}$")
    
    # Values with qualifiers
    assert regex.match("generally green")
    assert regex.match("mostly red")
    assert regex.match("usually blue")
    assert regex.match("sparsely purple")
    assert regex.match("densely green")
    assert regex.match("+- yellow")


def test_match_with_conjunctions():
    """Test matching values with conjunctions."""
    pattern = generate_attribute_regex(value_words=color_value_words)
    regex = re.compile(f"^{pattern}$")
    
    # Values with conjunctions
    assert regex.match("green and red")
    assert regex.match("green or yellow")
    assert regex.match("blue to purple")


def test_match_invalid_values():
    """Test matching invalid values."""
    pattern = generate_attribute_regex(value_words=color_value_words)
    regex = re.compile(f"^{pattern}$")
    
    # Should not match values not in the allowed list
    assert not regex.match("round")
    assert not regex.match("triangular")
    assert not regex.match("hairy")


def test_numeric_basic_ranges():
    """Test matching basic numeric ranges."""
    pattern = generate_numeric_regex()
    regex = re.compile(f"^{pattern}$")
    
    # Basic ranges
    assert regex.match("1--5 mm")
    assert regex.match("10--20 cm")
    assert regex.match("0--100 m")
    
    # Ranges without units
    assert regex.match("1--5")
    assert regex.match("10--20")


def test_numeric_with_qualifiers():
    """Test matching numeric ranges with prefix qualifiers."""
    pattern = generate_numeric_regex()
    regex = re.compile(f"^{pattern}$")
    
    # Ranges with qualifiers
    assert regex.match("generally 1--5 mm")
    assert regex.match("mostly 10--20 cm")
    assert regex.match("usually 0--100 m")
    assert regex.match("ca. 5--10 mm")
    assert regex.match("approximately 1--5 cm")
    assert regex.match("about 3--7 mm")


def test_numeric_with_decimals():
    """Test matching numeric ranges with decimal values."""
    pattern = generate_numeric_regex(allow_decimal=True)
    regex = re.compile(f"^{pattern}$")
    
    # Ranges with decimals
    assert regex.match("1.5--5.5 mm")
    assert regex.match("0.5--2.0 cm")
    assert regex.match("generally 1.0--3.5 mm")
    
    # Test with decimals disabled
    pattern_no_decimal = generate_numeric_regex(allow_decimal=False)
    regex_no_decimal = re.compile(f"^{pattern_no_decimal}$")
    
    assert not regex_no_decimal.match("1.5--5.5 mm")
    assert regex_no_decimal.match("1--5 mm")


def test_numeric_with_parenthetical():
    """Test matching numeric ranges with parenthetical values."""
    pattern = generate_numeric_regex(allow_parenthetical=True)
    regex = re.compile(f"^{pattern}$")
    
    # Ranges with parenthetical values
    assert regex.match("1--5(10) mm")
    assert regex.match("3--8(12) cm")
    assert regex.match("generally 2--6(9) mm")
    
    # Test with parenthetical disabled
    pattern_no_paren = generate_numeric_regex(allow_parenthetical=False)
    regex_no_paren = re.compile(f"^{pattern_no_paren}$")
    
    assert not regex_no_paren.match("1--5(10) mm")
    assert regex_no_paren.match("1--5 mm")


def test_numeric_invalid_ranges():
    """Test matching invalid numeric ranges."""
    pattern = generate_numeric_regex()
    regex = re.compile(f"^{pattern}$")
    
    # Should not match these formats
    assert not regex.match("1-5 mm")       # Hyphen instead of en-dash
    assert not regex.match("1 to 5 mm")    # Text conjunction instead of en-dash
    assert not regex.match("green")        # Non-numeric value
    assert not regex.match("5 mm")         # Single value, not a range
    assert not regex.match("1--5--10 mm")  # Multiple ranges
    assert not regex.match("1--5 meters")  # Unit not in default list
