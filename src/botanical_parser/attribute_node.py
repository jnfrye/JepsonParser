"""
Attribute node class representing properties of botanical structures.
"""
from typing import List, Dict, Optional
from .botanical_node import BotanicalNode


class AttributeNode(BotanicalNode):
    """
    Represents an attribute of a botanical structure (e.g., Color, Shape, Size).
    
    An attribute node contains one or more values.
    """
    
    def __init__(self, name: str, values: Optional[List['AttributeValue']] = None):
        """
        Initialize an attribute node.
        
        Args:
            name: The name of this attribute.
            values: Optional list of values for this attribute.
        """
        super().__init__(name)
        self.values: List['AttributeValue'] = values or []
    
    def add_value(self, value: 'AttributeValue') -> None:
        """
        Add a value to this attribute.
        
        Args:
            value: The value to add.
        """
        self.values.append(value)
    
    def to_dict(self) -> Dict:
        """
        Convert attribute node to dictionary representation.
        
        Returns:
            Dictionary representation of the attribute node.
        """
        return {
            'name': self.name,
            'type': 'attribute',
            'values': [val.to_dict() for val in self.values]
        }
