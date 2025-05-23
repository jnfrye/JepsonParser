"""
Tests for the node classes.
"""
import pytest
from botanical_parser.structure_node import StructureNode
from botanical_parser.attribute_node import AttributeNode
from botanical_parser.attribute_value import AttributeValue


def test_structure_node_creation():
    """Test that a structure node can be created."""
    node = StructureNode("Leaf")
    assert node.name == "Leaf"
    assert len(node.attributes) == 0
    assert len(node.children) == 0


def test_structure_node_add_attribute():
    """Test that attributes can be added to a structure node."""
    node = StructureNode("Leaf")
    attr = AttributeNode("Color")
    node.add_attribute(attr)
    
    assert len(node.attributes) == 1
    assert node.attributes[0] is attr


def test_structure_node_add_child():
    """Test that child structures can be added to a structure node."""
    parent = StructureNode("Plant")
    child = StructureNode("Leaf")
    parent.add_child(child)
    
    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_structure_node_find_attributes():
    """Test finding attributes by name."""
    node = StructureNode("Leaf")
    color_attr = AttributeNode("Color")
    shape_attr = AttributeNode("Shape")
    size_attr = AttributeNode("Size")
    
    node.add_attribute(color_attr)
    node.add_attribute(shape_attr)
    node.add_attribute(size_attr)
    
    color_results = node.find_attributes("Color")
    assert len(color_results) == 1
    assert color_results[0] is color_attr
    
    # Test case insensitivity
    shape_results = node.find_attributes("shape")
    assert len(shape_results) == 1
    assert shape_results[0] is shape_attr
    
    # Test no match
    texture_results = node.find_attributes("Texture")
    assert len(texture_results) == 0


def test_structure_node_find_children():
    """Test finding child structures by name."""
    parent = StructureNode("Plant")
    leaf = StructureNode("Leaf")
    stem = StructureNode("Stem")
    flower = StructureNode("Flower")
    
    parent.add_child(leaf)
    parent.add_child(stem)
    parent.add_child(flower)
    
    leaf_results = parent.find_children("Leaf")
    assert len(leaf_results) == 1
    assert leaf_results[0] is leaf
    
    # Test case insensitivity
    stem_results = parent.find_children("stem")
    assert len(stem_results) == 1
    assert stem_results[0] is stem
    
    # Test no match
    root_results = parent.find_children("Root")
    assert len(root_results) == 0


def test_structure_node_to_dict():
    """Test converting a structure node to a dictionary."""
    plant = StructureNode("Plant")
    
    # Add attributes
    color_attr = AttributeNode("Color", [AttributeValue("green")])
    plant.add_attribute(color_attr)
    
    # Add child with its own attribute
    leaf = StructureNode("Leaf")
    leaf_shape = AttributeNode("Shape", [AttributeValue("ovate")])
    leaf.add_attribute(leaf_shape)
    plant.add_child(leaf)
    
    # Convert to dictionary
    plant_dict = plant.to_dict()
    
    # Check structure
    assert plant_dict["name"] == "Plant"
    assert plant_dict["type"] == "structure"
    assert len(plant_dict["attributes"]) == 1
    assert len(plant_dict["children"]) == 1
    
    # Check attribute
    attr_dict = plant_dict["attributes"][0]
    assert attr_dict["name"] == "Color"
    assert attr_dict["type"] == "attribute"
    assert len(attr_dict["values"]) == 1
    assert attr_dict["values"][0]["raw_value"] == "green"
    
    # Check child
    child_dict = plant_dict["children"][0]
    assert child_dict["name"] == "Leaf"
    assert child_dict["type"] == "structure"
    assert len(child_dict["attributes"]) == 1
    assert child_dict["attributes"][0]["name"] == "Shape"
    assert child_dict["attributes"][0]["values"][0]["raw_value"] == "ovate"


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
    
    assert start.is_range_start is True
    assert start.is_range_end is False
    assert end.is_range_start is False
    assert end.is_range_end is True


def test_attribute_value_to_dict():
    """Test converting an attribute value to a dictionary."""
    value = AttributeValue("5", unit="cm", is_range_start=True)
    
    value_dict = value.to_dict()
    
    assert value_dict["raw_value"] == "5"
    assert value_dict["unit"] == "cm"
    assert value_dict["is_range_start"] is True
    assert value_dict["is_range_end"] is False
