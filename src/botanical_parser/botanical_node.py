"""
Base class for all botanical nodes.
"""
from abc import ABC, abstractmethod
from typing import Dict


class BotanicalNode(ABC):
    """Base abstract class for all nodes in the botanical description tree."""
    
    def __init__(self, name: str):
        """
        Initialize a botanical node.
        
        Args:
            name: The name of this node.
        """
        self.name = name
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Convert node to dictionary representation.
        
        Returns:
            Dictionary representation of the node.
        """
        pass
