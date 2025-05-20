from src.jepson_parser import parse_jepson_description
from src.feature_matcher import FeatureExtractor
from src.feature_node import FeatureNode

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
    assert any([c.name == 'Growth Form' and 'shrub or thicket-forming' == c.value for c in habit_general.children])
    assert any([c.name == 'Height' and '8--25 dm' == c.value for c in habit_general.children])

    # Check detailed Stem section
    stem = next(child for child in tree.children if child.name == 'Stem')
    prickle = next(child for child in stem.children if child.name == 'Prickle')
    assert any([c.name == 'Count' and 'few to many' == c.value for c in prickle.children])
    assert any([c.name == 'Grouping' and 'paired or not' == c.value for c in prickle.children])
    assert any([c.name == 'Length' and '3--15 mm' == c.value for c in prickle.children])
    assert any([c.name == 'Shape' and 'thick-based and compressed' == c.value for c in prickle.children])
    assert any([c.name == 'Curvature' and 'generally curved (straight)' == c.value for c in prickle.children])

    # Check detailed Leaf section
    leaf = next(child for child in tree.children if child.name == 'Leaf')
    axis = next((c for c in leaf.children if c.name == 'Axis'), None)
    assert axis is not None
    assert any(gr.name == 'Trichome' for gr in axis.children)
