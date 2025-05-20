from src.feature_matcher import FeatureExtractor
from src.feature_node import FeatureNode
import re
from typing import List, Optional, Dict


def get_jepson_feature_hierarchy():
    return FeatureExtractor(
        'TaxonDescription', r'.*', [
        FeatureExtractor(
            'Habit', r'^Habit:', [
                FeatureExtractor('General', r'.+', [
                    FeatureExtractor('Height', r'\d+--\d+ ?[a-zA-Z]+'),
                    FeatureExtractor('Growth Form', r'shrub|thicket-forming')
                ], split=r','),
            ], split=r';', consume_pattern=True),
        FeatureExtractor(
            'Stem', r'^Stem:', [
                FeatureExtractor('Prickle', r'prickles', [
                    FeatureExtractor('Count', r'few|many'),
                    FeatureExtractor('Grouping', r'paired'),
                    FeatureExtractor('Length', r'\d+--\d+ ?mm'),
                    FeatureExtractor('Shape', r'thick-based|compressed'),
                    FeatureExtractor('Curvature', r'curved|straight'),
                ], split=r',', consume_pattern=True)
            ], split=r';', consume_pattern=True),
        FeatureExtractor(
            'Leaf', r'^Leaf:', [
                FeatureExtractor('Axis', r'^axis', [
                    FeatureExtractor('Trichome', r'shaggy-hairy|glabrous', [
                        FeatureExtractor('Form', r'shaggy-hairy|glabrous'),
                        FeatureExtractor('Length', r'hairs? to ([^,;]+)'),
                        FeatureExtractor('Glandularity', r'glandless|glandular')
                    ])
                ], split=r',', consume_pattern=True)
            ], split=r';', consume_pattern=True)
        ], split=r'\.\s|; (?=Elevation)')

def parse_jepson_description(description: str) -> FeatureNode:
    """
    Fully data-driven parser for Jepson eFlora taxon descriptions using FeatureExtractor hierarchy.
    The top-level FeatureExtractor is responsible for splitting into sections and delegating extraction.
    """
    # Create a root FeatureExtractor that matches all top-level sections (Habit, Stem, Leaf, etc.)
    feature_matcher_tree = get_jepson_feature_hierarchy()
    return feature_matcher_tree.extract(description)

# Example usage (for testing)
if __name__ == "__main__":
    desc = '''Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight). Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not. Inflorescence: (1)3--30(50)-flowered; pedicels generally +- 5--20 mm, generally +- hairy, glandless. Flower: hypanthium 3--5.5 mm wide at flower, glabrous to sparsely hairy, glandless, neck 2--4.5 mm wide; sepals glandular or not, entire, tip generally +- equal to body, entire; petals generally 15--25 mm, pink; pistils 20--40. Fruit: generally 8--15(20) mm wide, generally (ob)ovoid; sepals generally erect, persistent; achenes generally 3.5--4.5 mm. Chromosomes: n=14.\nEcology: Generally +- moist areas, especially streambanks; Elevation: < 1800 m. Bioregional Distribution: CA-FP (exc CaRH, SNH, Teh); Distribution Outside California: southern Oregon, northern Baja California. Flowering Time: Feb--Nov'''
    tree = parse_jepson_description(desc)
    print(tree)
