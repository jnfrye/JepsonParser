from typing import List, Optional, Dict
from src.feature_value import FeatureValue

class FeatureNode:
    def __init__(self, name: str, values: Optional[List[FeatureValue]] = None):
        self.name = name
        # List of FeatureValue objects, capturing all values for this feature
        self.values: List[FeatureValue] = values if values is not None else []
        self.children: List['FeatureNode'] = []

    @property
    def value(self) -> Optional[str]:
        """Backward compatibility: returns the raw_value of the first FeatureValue, or None."""
        if self.values:
            return self.values[0].raw_value
        return None

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
            'values': [vars(v) for v in self.values],
            'children': [c.to_dict() for c in self.children]
        }

    def __repr__(self):
        return f"FeatureNode(name={self.name!r}, values={self.values!r}, children={self.children!r})"
