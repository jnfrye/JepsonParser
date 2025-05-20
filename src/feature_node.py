from typing import List, Optional, Dict

class FeatureNode:
    def __init__(self, name: str, value: Optional[str] = None):
        self.name = name
        self.value = value
        self.children: List['FeatureNode'] = []

    def add_child(self, child: 'FeatureNode'):
        self.children.append(child)

    def find(self, name: str) -> List['FeatureNode']:
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
        return f"FeatureNode(name={self.name!r}, value={self.value!r}, children={self.children!r})"
