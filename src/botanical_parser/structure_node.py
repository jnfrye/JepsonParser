"""
Structure node class representing botanical structures like Leaf, Stem, etc.
"""
from typing import List, Dict, Optional
from .botanical_node import BotanicalNode


class StructureNode(BotanicalNode):
    """
    Represents a botanical structure (e.g., Leaf, Stem, Flower).
    
    A structure node can have attributes (properties) and child structures.
    """
    
    def __init__(self, name: str):
        """
        Initialize a structure node.
        
        Args:
            name: The name of this structure.
        """
        super().__init__(name)
        self.attributes: List['AttributeNode'] = []
        self.children: List['StructureNode'] = []
    
    def add_attribute(self, attr: 'AttributeNode') -> None:
        """
        Add an attribute to this structure.
        
        Args:
            attr: The attribute to add.
        """
        self.attributes.append(attr)
    
    def add_child(self, child: 'StructureNode') -> None:
        """
        Add a child structure to this structure.
        
        Args:
            child: The child structure to add.
        """
        self.children.append(child)
    
    def find_attributes(self, name: str) -> List['AttributeNode']:
        """
        Find all attributes with the given name.
        
        Args:
            name: The name of the attribute to find.
            
        Returns:
            List of matching attribute nodes.
        """
        return [attr for attr in self.attributes if attr.name.lower() == name.lower()]
    
    def find_children(self, name: str) -> List['StructureNode']:
        """
        Find all child structures with the given name.
        
        Args:
            name: The name of the child structure to find.
            
        Returns:
            List of matching structure nodes.
        """
        return [child for child in self.children if child.name.lower() == name.lower()]
    
    def to_dict(self) -> Dict:
        """
        Convert structure node to dictionary representation.
        
        Returns:
            Dictionary representation of the structure node.
        """
        return {
            'name': self.name,
            'type': 'structure',
            'attributes': [attr.to_dict() for attr in self.attributes],
            'children': [child.to_dict() for child in self.children]
        }
