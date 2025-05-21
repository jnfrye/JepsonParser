from src.jepson_parser import parse_jepson_description
from src.feature_extractor import FeatureExtractor
from src.feature_node import FeatureNode
from src.feature_value import FeatureValue

def test_parse_jepson_description_tree():
    desc = '''Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight). Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not. Inflorescence: (1)3--30(50)-flowered; pedicels generally +- 5--20 mm, generally +- hairy, glandless. Flower: hypanthium 3--5.5 mm wide at flower, glabrous to sparsely hairy, glandless, neck 2--4.5 mm wide; sepals glandular or not, entire, tip generally +- equal to body, entire; petals generally 15--25 mm, pink; pistils 20--40. Fruit: generally 8--15(20) mm wide, generally (ob)ovoid; sepals generally erect, persistent; achenes generally 3.5--4.5 mm. Chromosomes: n=14.\nEcology: Generally +- moist areas, especially streambanks; Elevation: < 1800 m. Bioregional Distribution: CA-FP (exc CaRH, SNH, Teh); Distribution Outside California: southern Oregon, northern Baja California. Flowering Time: Feb--Nov'''
    tree = parse_jepson_description(desc)
    # Check root node
    assert tree.name == 'TaxonDescription'
    # Check detailed Habit section
    habit = next(child for child in tree.children if child.name == 'Habit')
    assert habit.children
    habit_general = next(child for child in habit.children if child.name == 'General')
    assert habit_general.children
    # Growth Form: shrub or thicket-forming
    growth_form_node = next((c for c in habit_general.children if c.name == 'Growth Form'), None)
    assert growth_form_node is not None
    assert len(growth_form_node.values) == 2
    assert growth_form_node.values[0].raw_value == 'shrub'
    assert growth_form_node.values[1].raw_value == 'thicket-forming'

    # Height: 8--25 dm
    height_node = next((c for c in habit_general.children if c.name == 'Height'), None)
    assert height_node is not None
    assert len(height_node.values) == 2
    assert height_node.values[0].raw_value == '8'
    assert height_node.values[0].is_range_start is True
    assert height_node.values[1].raw_value == '25 dm'
    assert height_node.values[1].is_range_start is False

    # Check detailed Stem section
    stem = next(child for child in tree.children if child.name == 'Stem')
    prickle = next(child for child in stem.children if child.name == 'Prickle')
    # Count
    count_node = next((c for c in prickle.children if c.name == 'Count'), None)
    assert count_node is not None
    assert count_node.values[0].raw_value == 'few'
    # Grouping
    grouping_node = next((c for c in prickle.children if c.name == 'Grouping'), None)
    assert grouping_node is not None
    assert grouping_node.values[0].raw_value == 'paired'
    # Length: 3--15 mm
    length_node = next((c for c in prickle.children if c.name == 'Length'), None)
    assert length_node is not None
    assert len(length_node.values) == 2
    assert length_node.values[0].raw_value == '3'
    assert length_node.values[0].is_range_start is True
    assert length_node.values[1].raw_value == '15 mm'
    assert length_node.values[1].is_range_start is False
    # Shape
    shape_node = next((c for c in prickle.children if c.name == 'Shape'), None)
    assert shape_node is not None
    assert shape_node.values[0].raw_value == 'thick-based and compressed'
    # Curvature
    curvature_node = next((c for c in prickle.children if c.name == 'Curvature'), None)
    assert curvature_node is not None
    assert curvature_node.values[0].raw_value == 'generally curved (straight)'

    # Check detailed Leaf section
    leaf = next(child for child in tree.children if child.name == 'Leaf')
    axis = next((c for c in leaf.children if c.name == 'Axis'), None)
    assert axis is not None
    assert any(gr.name == 'Trichome' for gr in axis.children)
