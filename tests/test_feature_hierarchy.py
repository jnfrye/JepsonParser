from src.jepson_parser import get_habit_feature_hierarchy, get_stem_feature_hierarchy, get_leaf_feature_hierarchy
import logging
logging.basicConfig(level=logging.DEBUG, force=True)

from src.feature_node import FeatureNode

def test_habit_feature_hierarchy():
    extractor = get_habit_feature_hierarchy()
    text = 'Habit: shrub or thicket-forming, 8--25 dm.'
    node = extractor.extract(text)
    assert node.name == 'Habit'
    general = next((c for c in node.children if c.name == 'General'), None)
    assert general is not None
    # Should find both Growth Form and Height
    assert any(c.name == 'Growth Form' and 'shrub or thicket-forming' in c.value for c in general.children)
    assert any(c.name == 'Height' and '8--25 dm' in c.value for c in general.children)

def test_stem_feature_hierarchy():
    extractor = get_stem_feature_hierarchy()
    text = 'Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight).'
    node = extractor.extract(text)
    assert node.name == 'Stem'
    prickle = next((c for c in node.children if c.name == 'Prickle'), None)
    assert prickle is not None
    # Should find Count, Grouping, Length, Shape, Curvature
    assert any(c.name == 'Count' and 'few' in c.value for c in prickle.children)
    assert any(c.name == 'Grouping' and 'paired' in c.value for c in prickle.children)
    assert any(c.name == 'Length' and '3--15 mm' in c.value for c in prickle.children)
    assert any(c.name == 'Shape' and 'thick-based' in c.value for c in prickle.children)
    assert any(c.name == 'Curvature' and 'curved' in c.value for c in prickle.children)

def test_leaf_feature_hierarchy():
    extractor = get_leaf_feature_hierarchy()
    text = 'Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not.'
    node = extractor.extract(text)
    assert node.name == 'Leaf'
    axis = next((c for c in node.children if c.name == 'Axis'), None)
    assert axis is not None
    trichome = next((c for c in axis.children if c.name == 'Trichome'), None)
    assert trichome is not None
    # Should find Form, Length, Glandularity
    assert any(c.name == 'Form' and ('shaggy-hairy' in c.value or 'glabrous' in c.value) for c in trichome.children)
    assert any(c.name == 'Length' and '1 mm' in c.value for c in trichome.children)
    assert any(c.name == 'Glandularity' and ('glandless' in c.value or 'glandular' in c.value) for c in trichome.children)
