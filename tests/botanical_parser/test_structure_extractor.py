"""
Tests for the StructureExtractor class.
"""
import pytest
from src.botanical_parser.structure_extractor import StructureExtractor
from src.botanical_parser.attribute_extractor import AttributeExtractor
from src.botanical_parser.attribute_node import AttributeNode
from src.botanical_parser.attribute_value import AttributeValue


def test_structure_extractor_simple():
    """Test extracting a simple structure."""
    extractor = StructureExtractor(
        name="Leaf",
        pattern=r"Leaf:\s*(.+?)(?=\n|$)",
        attribute_extractors=[
            AttributeExtractor("Color", r"(green|red|yellow)")  # Matches known color values directly
        ]
    )
    
    text = "Leaf: green.\nStem: brown."
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Leaf"
    assert len(node.attributes) == 1
    assert node.attributes[0].name == "Color"
    assert node.attributes[0].values[0].raw_value == "green"


def test_structure_extractor_no_match():
    """Test behavior when the structure pattern doesn't match."""
    extractor = StructureExtractor(
        name="Fruit",
        pattern=r"Fruit:\s*(.+?)(?=\n|$)"
    )
    
    text = "Leaf: The leaf is green.\nStem: The stem is brown."
    
    node = extractor.extract(text)
    
    assert node is None


def test_structure_extractor_with_children():
    """Test extracting a structure with child structures."""
    leaflet_extractor = StructureExtractor(
        name="Leaflet",
        pattern=r"leaflets\s+(.+?)(?=;|$)",
        attribute_extractors=[
            AttributeExtractor("Count", r"(\d+--\d+)")
        ]
    )
    
    leaf_extractor = StructureExtractor(
        name="Leaf",
        pattern=r"Leaf:\s*(.+?)(?=\n|$)",
        child_extractors=[leaflet_extractor]
    )
    
    text = "Leaf: leaflets 5--7, green.\nStem: brown."  # Jepson-style text
    
    node = leaf_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Leaf"
    assert len(node.children) == 1
    assert node.children[0].name == "Leaflet"
    assert len(node.children[0].attributes) == 1
    assert node.children[0].attributes[0].name == "Count"
    assert node.children[0].attributes[0].values[0].raw_value == "5"
    assert node.children[0].attributes[0].values[1].raw_value == "7"


def test_structure_extractor_root_level():
    """Test extracting using a root-level structure extractor."""
    color_extractor = AttributeExtractor("Color", r"(green|red|yellow|brown)")  # Shared color extractor

    leaf_extractor = StructureExtractor(
        name="Leaf",
        pattern=r"Leaf:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[
            color_extractor
        ]
    )
    
    stem_extractor = StructureExtractor(
        name="Stem",
        pattern=r"Stem:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[color_extractor]
    )
    
    root_extractor = StructureExtractor(
        name="Plant",
        pattern=None,
        child_extractors=[leaf_extractor, stem_extractor]
    )
    
    text = "Leaf: green.\nStem: brown."
    
    node = root_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Plant"
    assert len(node.children) == 2
    
    # Check leaf
    leaf = node.children[0]
    assert leaf.name == "Leaf"
    assert len(leaf.attributes) == 1
    assert leaf.attributes[0].name == "Color"
    assert leaf.attributes[0].values[0].raw_value == "green"
    
    # Check stem
    stem = node.children[1]
    assert stem.name == "Stem"
    assert len(stem.attributes) == 1
    assert stem.attributes[0].name == "Color"
    assert stem.attributes[0].values[0].raw_value == "brown"


def test_overlapping_child_structures():
    """Test handling of overlapping child structure regions."""
    first_extractor = StructureExtractor(
        name="First",
        pattern=r"first\s+(.+?)(?=\n|$)",
    )
    
    second_extractor = StructureExtractor(
        name="Second",
        pattern=r"second\s+(.+?)(?=\n|$)"
    )
    
    parent_extractor = StructureExtractor(
        name="Parent",
        pattern=r"Parent:\s*(.+?)(?=\n\w+:|$)",
        child_extractors=[first_extractor, second_extractor]
    )
    
    # Create text with overlapping potential matches
    text = "Parent: first description overlapping second description."
    
    node = parent_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Parent"
    assert len(node.children) == 2
    
    # Verify first child
    assert node.children[0].name == "First"
    
    # Verify second child
    assert node.children[1].name == "Second"
