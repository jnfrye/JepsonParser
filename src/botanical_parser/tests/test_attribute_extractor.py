"""
Tests for the AttributeExtractor class.
"""
import pytest
from botanical_parser.attribute_extractor import AttributeExtractor
from botanical_parser.attribute_node import AttributeNode
from botanical_parser.attribute_value import AttributeValue


def test_attribute_extractor_simple():
    """Test extracting a simple attribute."""
    extractor = AttributeExtractor("Color", r"^(green|yellow)$")  # Simplified regex for direct value
    text = "green"  # Text passed to AttributeExtractor is already pre-processed
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Color"
    assert len(node.values) == 1
    assert node.values[0].raw_value == "green"


def test_attribute_extractor_no_match():
    """Test behavior when the pattern doesn't match."""
    extractor = AttributeExtractor("Color", r"^(green|yellow)$")  # Expects only green or yellow
    text = "blue"  # This text won't match the pattern
    
    node = extractor.extract(text)
    
    assert node is None


def test_attribute_extractor_no_pattern():
    """Test behavior when no pattern is provided."""
    extractor = AttributeExtractor("Color")
    text = "The leaf color green."
    
    node = extractor.extract(text)
    
    assert node is None


def test_attribute_extractor_range():
    """Test extracting a range attribute."""
    extractor = AttributeExtractor("Height", r"^(\d+\s*--\s*\d+\s*[a-zA-Z]*)$") # Pattern for the value itself
    text = "5--10 cm"  # Pre-processed text
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Height"
    assert len(node.values) == 2
    
    # Check range values
    assert node.values[0].raw_value == "5"
    assert node.values[0].unit == "cm"
    assert node.values[0].is_range_start is True
    
    assert node.values[1].raw_value == "10"
    assert node.values[1].unit == "cm"
    assert node.values[1].is_range_end is True


def test_attribute_extractor_or_values():
    """Test extracting an attribute with OR values."""
    extractor = AttributeExtractor("Growth Form", r"^([\w\s-]+(?:\s+or\s+[\w\s-]+)+)$") # Pattern for the value
    text = "shrub or thicket-forming"  # Pre-processed text
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Growth Form"
    assert len(node.values) == 2
    assert node.values[0].raw_value == "shrub"
    assert node.values[1].raw_value == "thicket-forming"


def test_attribute_extractor_with_unit():
    """Test extracting an attribute with a unit."""
    extractor = AttributeExtractor("Size", r"^(\d+\s*[a-zA-Z]+)$") # Pattern for the value
    text = "5 mm"  # Pre-processed text
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Size"
    assert len(node.values) == 1
    assert node.values[0].raw_value == "5"
    assert node.values[0].unit == "mm"
