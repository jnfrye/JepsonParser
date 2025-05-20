import re
from typing import List, Optional, Dict

class DescriptionNode:
    def __init__(self, name: str, value: Optional[str] = None):
        self.name = name
        self.value = value
        self.children: List['DescriptionNode'] = []

    def add_child(self, child: 'DescriptionNode'):
        self.children.append(child)

    def find(self, name: str) -> List['DescriptionNode']:
        """Recursively find all nodes with the given name."""
        result = []
        if self.name.lower() == name.lower():
            result.append(self)
        for child in self.children:
            result.extend(child.find(name))
        return result

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'value': self.value,
            'children': [c.to_dict() for c in self.children]
        }

    def __repr__(self):
        return f"DescriptionNode(name={self.name!r}, value={self.value!r}, children={self.children!r})"

def _clean_value(val):
    return val.rstrip('.').strip()

class FeatureMatcher:
    def __init__(self, name: str, pattern, children=None, split=None, consume_pattern=False):
        self.name = name
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern, re.IGNORECASE)
        else:
            self.pattern = pattern
        
        self.children = children or []
        self.split = split
        self.consume_pattern = consume_pattern

    def match(self, text):
        return self.pattern.match(text)

    def extract(self, text):
        """
        Recursively extract features from text using this matcher and its children.
        Returns a DescriptionNode or None if not matched.
        """
        node = DescriptionNode(self.name)
        if self.children:
            if self.split:
                parts = [p.strip() for p in re.split(self.split, text) if p.strip()]
            else:
                parts = [text.strip()]
            
            for part in parts:
                if not part:
                    continue
                matched = False

                for child in self.children:
                    match = child.pattern.search(part)
                    if match:
                        matched = True
                        if child.consume_pattern:
                            part = part[match.end():]
                        child_node = child.extract(part)
                        node.add_child(child_node)
                        break
                
                if not matched and self.children:
                    # If no child matched, just add as a generic feature
                    node.add_child(DescriptionNode('Unmatched', part))
        else:
            node.value = _clean_value(text)
        
        return node

def get_jepson_feature_hierarchy():
    return FeatureMatcher(
        'TaxonDescription', r'.*', [
        FeatureMatcher(
            'Habit', r'^Habit:', [
                FeatureMatcher('General', r'.+', [
                    FeatureMatcher('Height', r'\d+--\d+ ?[a-zA-Z]+'),
                    FeatureMatcher('Growth Form', r'shrub|thicket-forming')
                ], split=r','),
            ], split=r';', consume_pattern=True),
        FeatureMatcher(
            'Stem', r'^Stem:', [
                FeatureMatcher('Prickle', r'prickles', [
                    FeatureMatcher('Count', r'few|many'),
                    FeatureMatcher('Grouping', r'paired'),
                    FeatureMatcher('Length', r'\d+--\d+ ?mm'),
                    FeatureMatcher('Shape', r'thick-based|compressed'),
                    FeatureMatcher('Curvature', r'curved|straight'),
                ], split=r',', consume_pattern=True)
            ], split=r';', consume_pattern=True),
        FeatureMatcher(
            'Leaf', r'^Leaf:', [
                FeatureMatcher('Axis', r'^axis', [
                    FeatureMatcher('Trichome', r'shaggy-hairy|glabrous', [
                        FeatureMatcher('Form', r'shaggy-hairy|glabrous'),
                        FeatureMatcher('Length', r'hairs? to ([^,;]+)'),
                        FeatureMatcher('Glandularity', r'glandless|glandular')
                    ])
                ], split=r',', consume_pattern=True)
            ], split=r';', consume_pattern=True)
        ], split=r'\.\s|; (?=Elevation)')

def parse_jepson_description(description: str) -> DescriptionNode:
    """
    Fully data-driven parser for Jepson eFlora taxon descriptions using FeatureMatcher hierarchy.
    The top-level FeatureMatcher is responsible for splitting into sections and delegating extraction.
    """
    # Create a root FeatureMatcher that matches all top-level sections (Habit, Stem, Leaf, etc.)
    feature_matcher_tree = get_jepson_feature_hierarchy()
    return feature_matcher_tree.extract(description)

# Example usage (for testing)
if __name__ == "__main__":
    desc = '''Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight). Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not. Inflorescence: (1)3--30(50)-flowered; pedicels generally +- 5--20 mm, generally +- hairy, glandless. Flower: hypanthium 3--5.5 mm wide at flower, glabrous to sparsely hairy, glandless, neck 2--4.5 mm wide; sepals glandular or not, entire, tip generally +- equal to body, entire; petals generally 15--25 mm, pink; pistils 20--40. Fruit: generally 8--15(20) mm wide, generally (ob)ovoid; sepals generally erect, persistent; achenes generally 3.5--4.5 mm. Chromosomes: n=14.\nEcology: Generally +- moist areas, especially streambanks; Elevation: < 1800 m. Bioregional Distribution: CA-FP (exc CaRH, SNH, Teh); Distribution Outside California: southern Oregon, northern Baja California. Flowering Time: Feb--Nov'''
    tree = parse_jepson_description(desc)
    print(tree)
