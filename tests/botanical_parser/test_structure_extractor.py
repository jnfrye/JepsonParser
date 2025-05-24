"""
Tests for the StructureExtractor class.
"""
import pytest
from src.botanical_parser.structure_extractor import StructureExtractor
from src.botanical_parser.attribute_extractor import QualitativeAttributeExtractor, NumericAttributeExtractor
from src.botanical_parser.attribute_node import AttributeNode
from src.botanical_parser.attribute_value import AttributeValue


def test_structure_extractor_simple():
    """Test extracting a simple structure."""
    extractor = StructureExtractor(
        name="Leaf",
        noun="Leaf:",
        attribute_extractors=[
            QualitativeAttributeExtractor("Color", value_words=["green", "red", "yellow"])
        ]
    )

    text = "Leaf: green.\nStem: brown."
    
    node = extractor.extract(text)
    
    assert node is not None
    assert node.name == "Leaf"
    assert len(node.attributes) == 1
    assert node.attributes[0].name == "Color"
    assert node.attributes[0].values[0] == AttributeValue("green")


def test_structure_extractor_no_match():
    """Test behavior when the structure pattern doesn't match."""
    extractor = StructureExtractor(
        name="Fruit",
        noun="Fruit:"
    )
    
    text = "Leaf: The leaf is green.\nStem: The stem is brown."
    
    node = extractor.extract(text)
    
    assert node is None


def test_structure_extractor_with_children():
    """Test extracting a structure with child structures."""
    leaflet_extractor = StructureExtractor(
        name="Leaflet",
        noun="leaflets",
        attribute_extractors=[
            NumericAttributeExtractor("Count", units=[])
        ]
    )
    
    leaf_extractor = StructureExtractor(
        name="Leaf",
        noun="Leaf:",
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
    color_extractor = QualitativeAttributeExtractor("Color", value_words=["green", "red", "yellow", "brown"])

    leaf_extractor = StructureExtractor(
        name="Leaf",
        noun="Leaf:",
        attribute_extractors=[color_extractor]
    )
    
    stem_extractor = StructureExtractor(
        name="Stem",
        noun="Stem:",
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
    assert leaf.attributes[0].values[0] == AttributeValue("green")
    
    # Check stem
    stem = node.children[1]
    assert stem.name == "Stem"
    assert len(stem.attributes) == 1
    assert stem.attributes[0].name == "Color"
    assert stem.attributes[0].values[0] == AttributeValue("brown")


def test_pattern_custom_keyword():
    """Test using a custom pattern with a required trailing keyword."""
    extractor = StructureExtractor(
        name="Leaf",
        pattern=r"Leaf:\s*(.+?)\s*\[special\]",
        attribute_extractors=[QualitativeAttributeExtractor("Color", value_words=["green", "yellow"])]
    )

    text = "Leaf: green [special]\nLeaf: yellow\nStem: brown."
    node = extractor.extract(text)
    assert node is not None
    assert node.name == "Leaf"
    assert len(node.attributes) == 1
    assert node.attributes[0].values[0] == AttributeValue("green")


def test_pattern_multiline_custom():
    """Test using a custom pattern to extract a multiline structure region."""
    extractor = StructureExtractor(
        name="Description",
        pattern=r"Description:\n((?:.+\n)+?)EndDescription",
        attribute_extractors=[]
    )

    text = "Description:\nThis is line one.\nThis is line two.\nEndDescription\nOther: ignored."
    node = extractor.extract(text)
    assert node is not None
    assert node.name == "Description"
    # The captured text should include both lines (without EndDescription)
    # You may want to check node.raw_text or similar, depending on implementation


def test_overlapping_child_structures():
    """Test handling of overlapping child structure regions."""
    first_extractor = StructureExtractor(
        name="First",
        noun="first"
    )
    
    second_extractor = StructureExtractor(
        name="Second",
        noun="second"
    )
    
    parent_extractor = StructureExtractor(
        name="Parent",
        noun="Parent:",
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
