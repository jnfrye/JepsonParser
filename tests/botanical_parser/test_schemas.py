"""
Tests for the schema definitions using real Jepson description data.
"""
import pytest
from src.botanical_parser.schemas import (
    get_habit_schema,
    get_stem_schema,
    get_leaf_schema,
    get_flower_schema,
    get_fruit_schema,
    get_jepson_schema
)
from src.botanical_parser.attribute_value import AttributeValue


def test_habit_schema():
    """Test extracting habit information from a real description."""
    text = "Habit: shrub or thicket-forming, 5--30 dm, generally erect."
    
    habit_extractor = get_habit_schema()
    node = habit_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Habit"
    
    # Test height extraction
    height_attr = node.find_attributes("Height")[0]
    assert height_attr.values[0] == AttributeValue("5", unit="dm", is_range_start=True)
    assert height_attr.values[1] == AttributeValue("30", unit="dm", is_range_end=True)
    
    # Test growth form extraction
    growth_form_attr = node.find_attributes("Growth Form")[0]
    assert growth_form_attr.values[0] == AttributeValue("shrub")
    assert growth_form_attr.values[1] == AttributeValue("thicket-forming")

    # Test erectness extraction
    erectness_attr = node.find_attributes("Erectness")[0]
    assert erectness_attr.values[0] == AttributeValue("erect")


def test_stem_schema_with_prickles():
    """Test extracting stem information with prickles from a real description."""
    text = "Stem: generally rough; prickles few or many, paired or not, 3--7 mm, thick-based or compressed, generally curved."
    
    stem_extractor = get_stem_schema()
    node = stem_extractor.extract(text)
    assert node.name == "Stem"
    
    # Test prickle child node
    prickle = node.find_children("Prickle")[0]
    
    # Test prickle attributes
    count_attr = prickle.find_attributes("Count")[0]
    assert count_attr.values[0] == AttributeValue("few")
    assert count_attr.values[1] == AttributeValue("many")
    
    grouping_attr = prickle.find_attributes("Grouping")[0]
    assert grouping_attr.values[0] == AttributeValue("paired")
    
    length_attr = prickle.find_attributes("Length")[0]
    assert length_attr.values[0] == AttributeValue("3", unit="mm", is_range_start=True)
    assert length_attr.values[1] == AttributeValue("7", unit="mm", is_range_end=True)
    
    shape_attr = prickle.find_attributes("Shape")[0]
    assert shape_attr.values[0] == AttributeValue("thick-based")
    assert shape_attr.values[1] == AttributeValue("compressed")
    
    curvature_attr = prickle.find_attributes("Curvature")[0]
    assert curvature_attr.values[0] == AttributeValue("curved")


def test_leaf_schema_with_leaflets():
    """Test extracting leaf information with leaflets from a real description."""
    text = "Leaf: axis +- shaggy-hairy, hairs to 1 mm, glandless or glandular; leaflets 5--7, hairy to glabrous; " \
           "terminal leaflet generally 15--35 mm, ovate-elliptic, widest at or below middle, tip rounded, " \
           "margins single- or double-toothed."
    
    leaf_extractor = get_leaf_schema()
    node = leaf_extractor.extract(text)
    assert node.name == "Leaf"
    assert len(node.children) == 3
    
    # Test axis child node
    axis = node.find_children("Axis")[0]
    
    trichome_attr = axis.find_attributes("Trichome Form")[0]
    assert trichome_attr.values[0] == AttributeValue("shaggy-hairy")
    
    hair_length_attr = axis.find_attributes("Hair Length")[0]
    assert hair_length_attr.values[0] == AttributeValue("1", unit="mm")
    
    glandularity_attr = axis.find_attributes("Glandularity")[0]
    assert glandularity_attr.values[0] == AttributeValue("glandless")
    assert glandularity_attr.values[1] == AttributeValue("glandular")
    
    # Test leaflet child node
    leaflet = node.find_children("Leaflet")[0]
    
    count_attr = leaflet.find_attributes("Count")[0]
    assert count_attr.values[0] == AttributeValue("5", is_range_start=True)
    assert count_attr.values[1] == AttributeValue("7", is_range_end=True)
    
    surface_attr = leaflet.find_attributes("Surface")[0]
    assert surface_attr.values[0] == AttributeValue("hairy")
    assert surface_attr.values[1] == AttributeValue("glabrous")
    
    # Test terminal leaflet child node
    terminal = node.find_children("Terminal Leaflet")[0]
    
    size_attr = terminal.find_attributes("Size")[0]
    assert size_attr.values[0] == AttributeValue("15", unit="mm", is_range_start=True)
    assert size_attr.values[1] == AttributeValue("35", unit="mm", is_range_end=True)
    
    shape_attr = terminal.find_attributes("Shape")[0]
    assert shape_attr.values[0] == AttributeValue("ovate")
    assert shape_attr.values[1] == AttributeValue("elliptic")
    
    width_pos_attr = terminal.find_attributes("Width Position")[0]
    assert width_pos_attr.values[0] == AttributeValue("below")
    
    tip_attr = terminal.find_attributes("Tip")[0]
    assert tip_attr.values[0] == AttributeValue("rounded")
    
    margin_attr = terminal.find_attributes("Margin")[0]
    assert margin_attr.values[0] == AttributeValue("toothed")


def test_flower_schema():
    """Test extracting flower information from a real description."""
    text = "Flower: hypanthium 5--8 mm wide, generally glabrous, glandular or not; " \
           "sepals glandular or not, entire; petals generally 10--18 mm, pink; " \
           "pistils 20--35."
    
    flower_extractor = get_flower_schema()
    node = flower_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Flower"
    assert len(node.children) == 4
    
    # Test hypanthium child node
    hypanthium = node.find_children("Hypanthium")[0]
    
    width_attr = hypanthium.find_attributes("Width")[0]
    assert width_attr.values[0] == AttributeValue("5", unit="mm", is_range_start=True)
    assert width_attr.values[1] == AttributeValue("8", unit="mm", is_range_end=True)
    
    surface_attr = hypanthium.find_attributes("Surface")[0]
    assert surface_attr.values[0] == AttributeValue("glabrous")
    
    glandularity_attr = hypanthium.find_attributes("Glandularity")[0]
    assert glandularity_attr.values[0] == AttributeValue("glandular")
    assert glandularity_attr.values[1] == AttributeValue("glandless")
    
    # Test sepal child node
    sepal = node.find_children("Sepal")[0]
    assert sepal.name == "Sepal"
    
    sepal_gland_attr = sepal.find_attributes("Glandularity")[0]
    assert sepal_gland_attr.values[0] == AttributeValue("glandular")
    assert sepal_gland_attr.values[1] == AttributeValue("glandless")
    
    margin_attr = sepal.find_attributes("Margin")[0]
    assert margin_attr.values[0] == AttributeValue("entire")
    
    # Test petal child node
    petal = node.find_children("Petal")[0]
    assert petal.name == "Petal"
    
    size_attr = petal.find_attributes("Size")[0]
    assert size_attr.values[0] == AttributeValue("10", unit="mm", is_range_start=True)
    assert size_attr.values[1] == AttributeValue("18", unit="mm", is_range_end=True)
    
    color_attr = petal.find_attributes("Color")[0]
    assert color_attr.values[0] == AttributeValue("pink")
    
    # Test pistil child node
    pistil = node.find_children("Pistil")[0]
    assert pistil.name == "Pistil"
    
    count_attr = pistil.find_attributes("Count")[0]
    assert count_attr.values[0] == AttributeValue("20", is_range_start=True)
    assert count_attr.values[1] == AttributeValue("35", is_range_end=True)


def test_fruit_schema():
    """Test extracting fruit information from a real description."""
    text = "Fruit: generally 7--10(12) mm wide, generally ovoid; sepals generally erect, persistent; " \
           "achenes generally 1.5--2.5 mm."
    
    fruit_extractor = get_fruit_schema()
    node = fruit_extractor.extract(text)
    
    assert node is not None
    assert node.name == "Fruit"
    
    # Test fruit attributes
    width_attr = node.find_attributes("Width")[0]
    assert width_attr.values[0] == AttributeValue("7", unit="mm", is_range_start=True)
    assert width_attr.values[1] == AttributeValue("10", unit="mm", is_range_end=True)
    
    shape_attr = node.find_attributes("Shape")[0]
    assert shape_attr.values[0] == AttributeValue("ovoid")
    
    # Test sepal child node
    sepal = node.find_children("Sepal")[0]
    assert sepal.name == "Sepal"
    
    position_attr = sepal.find_attributes("Position")[0]
    assert position_attr.values[0] == AttributeValue("erect")
    
    persistence_attr = sepal.find_attributes("Persistence")[0]
    assert persistence_attr.values[0] == AttributeValue("persistent")
    
    # Test achene child node
    achene = node.find_children("Achene")[0]
    assert achene.name == "Achene"
    
    size_attr = achene.find_attributes("Size")[0]
    assert size_attr.values[0] == AttributeValue("1.5", unit="mm", is_range_start=True)
    assert size_attr.values[1] == AttributeValue("2.5", unit="mm", is_range_end=True)
