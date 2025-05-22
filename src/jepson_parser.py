from src.feature_extractor import FeatureExtractor
from src.feature_node import FeatureNode
import re
from typing import List, Optional, Dict

from src.feature_schema import get_habit_feature_schema, get_stem_feature_schema, get_leaf_feature_schema, get_jepson_feature_schema

# Example usage (for testing)
if __name__ == "__main__":
    desc = '''Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight). Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not. Inflorescence: (1)3--30(50)-flowered; pedicels generally +- 5--20 mm, generally +- hairy, glandless. Flower: hypanthium 3--5.5 mm wide at flower, glabrous to sparsely hairy, glandless, neck 2--4.5 mm wide; sepals glandular or not, entire, tip generally +- equal to body, entire; petals generally 15--25 mm, pink; pistils 20--40. Fruit: generally 8--15(20) mm wide, generally (ob)ovoid; sepals generally erect, persistent; achenes generally 3.5--4.5 mm. Chromosomes: n=14.\nEcology: Generally +- moist areas, especially streambanks; Elevation: < 1800 m. Bioregional Distribution: CA-FP (exc CaRH, SNH, Teh); Distribution Outside California: southern Oregon, northern Baja California. Flowering Time: Feb--Nov'''
    schema = get_jepson_feature_schema()
    tree = schema.extract(desc)
    print(tree)
