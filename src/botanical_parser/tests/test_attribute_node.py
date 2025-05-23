"""
Tests for the AttributeNode and AttributeValue classes.
"""
import pytest
from botanical_parser.attribute_node import AttributeNode
from botanical_parser.attribute_value import AttributeValue


def test_attribute_node_creation():
    """Test that an attribute node can be created."""
    node = AttributeNode("Color")
    assert node.name == "Color"
    assert len(node.values) == 0


def test_attribute_node_with_values():
    """Test creating an attribute node with values."""
    values = [AttributeValue("red"), AttributeValue("green")]
    node = AttributeNode("Color", values)
    
    assert len(node.values) == 2
    assert node.values[0].raw_value == "red"
    assert node.values[1].raw_value == "green"


def test_attribute_node_add_value():
    """Test adding values to an attribute node."""
    node = AttributeNode("Size")
    node.add_value(AttributeValue("5", unit="cm"))
    
    assert len(node.values) == 1
    assert node.values[0].raw_value == "5"
    assert node.values[0].unit == "cm"


def test_attribute_node_to_dict():
    """Test converting an attribute node to a dictionary."""
    values = [
        AttributeValue("5", unit="cm", is_range_start=True),
        AttributeValue("10", unit="cm", is_range_end=True)
    ]
    node = AttributeNode("Size", values)
    
    node_dict = node.to_dict()
    
    assert node_dict["name"] == "Size"
    assert node_dict["type"] == "attribute"
    assert len(node_dict["values"]) == 2
    
    # Check first value
    val1 = node_dict["values"][0]
    assert val1["raw_value"] == "5"
    assert val1["unit"] == "cm"
    assert val1["is_range_start"] is True
    assert val1["is_range_end"] is False
    
    # Check second value
    val2 = node_dict["values"][1]
    assert val2["raw_value"] == "10"
    assert val2["unit"] == "cm"
    assert val2["is_range_start"] is False
    assert val2["is_range_end"] is True


def test_attribute_value_creation():
    """Test that an attribute value can be created."""
    value = AttributeValue("red")
    assert value.raw_value == "red"
    assert value.unit is None
    assert value.is_range_start is False
    assert value.is_range_end is False


def test_attribute_value_with_unit():
    """Test creating an attribute value with a unit."""
    value = AttributeValue("5", unit="mm")
    assert value.raw_value == "5"
    assert value.unit == "mm"


def test_attribute_value_as_range():
    """Test creating attribute values that form a range."""
    start = AttributeValue("5", unit="cm", is_range_start=True)
    end = AttributeValue("10", unit="cm", is_range_end=True)
    
    assert start.raw_value == "5"
    assert start.is_range_start is True
    assert end.raw_value == "10"
    assert end.is_range_end is True


def test_attribute_value_to_dict():
    """Test converting an attribute value to a dictionary."""
    value = AttributeValue("5", unit="cm", is_range_start=True)
    value_dict = value.to_dict()
    
    assert value_dict["raw_value"] == "5"
    assert value_dict["unit"] == "cm"
    assert value_dict["is_range_start"] is True
    assert value_dict["is_range_end"] is False
