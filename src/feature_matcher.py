import re
from src.feature_node import FeatureNode

class FeatureExtractor:
    def __init__(self, name: str, pattern, children=None, split=None, value_group=None):
        self.name = name
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern, re.IGNORECASE)
        else:
            self.pattern = pattern
        self.children = children or []
        self.split = split
        self.value_group = value_group

    def match(self, text):
        return self.pattern.match(text)

    def extract(self, text):
        """
        Recursively extract features from text using this matcher and its children.
        Returns a FeatureNode or None if not matched.
        """
        node = FeatureNode(self.name)
        if self.split:
            parts = [p.strip() for p in re.split(self.split, text) if p.strip()]
        else:
            parts = [text]
        for part in parts:
            part = part.strip()
            if not part:
                continue
            matched = False
            for child in self.children:
                m = child.pattern.search(part)
                if m:
                    value = m.group(child.value_group if child.value_group is not None else 0).strip()
                    value = part.rstrip('.')
                    child_node = child.extract(part)
                    if child_node:
                        child_node.value = value
                        node.add_child(child_node)
                    else:
                        node.add_child(FeatureNode(child.name, value))
                    matched = True
                    break
            if not matched and self.children:
                node.add_child(FeatureNode('Unmatched', part))
        return node
