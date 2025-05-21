from src.feature_schema import get_habit_feature_schema, get_stem_feature_schema, get_leaf_feature_schema
import logging
logging.basicConfig(level=logging.DEBUG, force=True)

from src.feature_node import FeatureNode

def test_habit_feature_schema():
    extractor = get_habit_feature_schema()
    text = 'Habit: shrub or thicket-forming, 8--25 dm.'
    node = extractor.extract(text)
    assert node.name == 'Habit'
    general = next((c for c in node.children if c.name == 'General'), None)
    assert general is not None
    # Should find both Growth Form and Height
    growth_form_node = next((c for c in general.children if c.name == 'Growth Form'), None)
    assert growth_form_node is not None
    assert len(growth_form_node.values) == 2
    assert growth_form_node.values[0].raw_value == 'shrub'
    assert growth_form_node.values[0].is_range_start is False
    assert growth_form_node.values[0].unit is None
    assert growth_form_node.values[1].raw_value == 'thicket-forming'
    assert growth_form_node.values[1].is_range_start is False
    assert growth_form_node.values[1].unit is None

    height_node = next((c for c in general.children if c.name == 'Height'), None)
    assert height_node is not None
    assert len(height_node.values) == 2
    assert height_node.values[0].raw_value == '8'
    assert height_node.values[0].is_range_start is True
    assert height_node.values[0].unit == 'dm'
    assert height_node.values[1].raw_value == '25'
    assert height_node.values[1].is_range_start is False
    assert height_node.values[1].unit == 'dm'


def test_stem_feature_schema():
    extractor = get_stem_feature_schema()
    text = 'Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight).'
    node = extractor.extract(text)
    assert node.name == 'Stem'
    prickle = next((c for c in node.children if c.name == 'Prickle'), None)
    assert prickle is not None
    # Should find Count, Grouping, Length, Shape, Curvature
    assert any(c.name == 'Count' and 'few' in c.value for c in prickle.children)
    assert any(c.name == 'Grouping' and 'paired' in c.value for c in prickle.children)

    length_node = next((c for c in prickle.children if c.name == 'Length'), None)
    assert length_node is not None
    assert len(length_node.values) == 2
    assert length_node.values[0].raw_value == '3'
    assert length_node.values[0].is_range_start is True
    assert length_node.values[0].unit == 'mm'
    assert length_node.values[1].raw_value == '15'
    assert length_node.values[1].is_range_start is False
    assert length_node.values[1].unit == 'mm'

    assert any(c.name == 'Shape' and 'thick-based' in c.value for c in prickle.children)
    assert any(c.name == 'Curvature' and 'curved' in c.value for c in prickle.children)

def test_leaf_feature_schema():
    extractor = get_leaf_feature_schema()
    text = 'Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not.'
    node = extractor.extract(text)
    assert node.name == 'Leaf'
    axis = next((c for c in node.children if c.name == 'Axis'), None)
    assert axis is not None
    trichome = next((c for c in axis.children if c.name == 'Trichome'), None)
    assert trichome is not None
    # Should find Form, Length, Glandularity
    assert any(c.name == 'Form' and ('shaggy-hairy' in c.value or 'glabrous' in c.value) for c in trichome.children)
    assert any(
        c.name == 'Length' and c.values and c.values[0].raw_value == '1' and c.values[0].unit == 'mm'
        for c in trichome.children)
    assert any(c.name == 'Glandularity' and ('glandless' in c.value or 'glandular' in c.value) for c in trichome.children)
