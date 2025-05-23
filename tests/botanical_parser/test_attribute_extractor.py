"""
Tests for the AttributeExtractor classes.
"""
import pytest
from src.botanical_parser.attribute_extractor import (
    create_attribute_extractor,
    NumericAttributeExtractor, 
    QualitativeAttributeExtractor
)
from src.botanical_parser.attribute_node import AttributeNode
from src.botanical_parser.attribute_value import AttributeValue


def test_attribute_extractor_simple():
    """Test extracting a simple attribute using QualitativeAttributeExtractor."""
    extractor = QualitativeAttributeExtractor(
        name="Color", 
        value_words=["green", "yellow"]
    )
    text = "green"  # Text passed to AttributeExtractor is already pre-processed
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Color"
    assert len(node.values) == 1
    assert node.values[0].raw_value == "green"


def test_attribute_extractor_no_match():
    """Test behavior when the pattern doesn't match."""
    extractor = QualitativeAttributeExtractor(
        name="Color", 
        value_words=["green", "yellow"]
    )
    text = "blue"  # This text won't match the pattern
    
    node = extractor.extract(text)
    
    assert node is None


def test_attribute_extractor_custom():
    """Test behavior with a custom pattern using the legacy constructor."""
    extractor = create_attribute_extractor("Color", r"(\w+)")
    text = "green"
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Color"
    assert len(node.values) == 1
    assert node.values[0].raw_value == "green"


def test_attribute_extractor_range():
    """Test extracting a range attribute using NumericAttributeExtractor."""
    extractor = NumericAttributeExtractor(
        name="Height", 
        units=["cm", "mm"]
    )
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
    """Test extracting an attribute with OR values using QualitativeAttributeExtractor."""
    extractor = QualitativeAttributeExtractor(
        name="Growth Form", 
        value_words=["shrub", "thicket-forming", "tree", "herb"],
        conjunctions=["or", "and"]
    )
    text = "shrub or thicket-forming"  # Pre-processed text
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Growth Form"
    assert len(node.values) == 2
    assert node.values[0].raw_value == "shrub"
    assert node.values[1].raw_value == "thicket-forming"


def test_attribute_extractor_with_unit():
    """Test extracting an attribute with a unit using NumericAttributeExtractor."""
    extractor = NumericAttributeExtractor(
        name="Size", 
        units=["mm", "cm"]
    )
    text = "5 mm"  # Pre-processed text
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Size"
    assert len(node.values) == 1
    assert node.values[0].raw_value == "5"
    assert node.values[0].unit == "mm"
