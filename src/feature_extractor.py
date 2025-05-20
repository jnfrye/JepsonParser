import re
from src.feature_node import FeatureNode


def _clean_value(val):
    return val.rstrip('.').strip()

class FeatureExtractor:
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
        Returns a FeatureNode or None if not matched.
        """
        node = FeatureNode(self.name)
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
                    node.add_child(FeatureNode('Unmatched', part))
        else:
            node.value = _clean_value(text)
        return node
