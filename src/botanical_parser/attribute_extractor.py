"""
Attribute extractor class for extracting attributes from botanical descriptions.
"""
import re
import logging
from typing import List, Optional, Dict, Pattern
from .attribute_node import AttributeNode
from .attribute_value import AttributeValue

# Configure logging
logger = logging.getLogger(__name__)


class AttributeExtractor:
    """
    Extracts botanical attributes from text.
    """
    
    def __init__(self, name: str, pattern: Optional[str] = None):
        """
        Initialize an attribute extractor.
        
        Args:
            name: The name of the attribute to extract.
            pattern: Regular expression pattern to match the attribute.
                     Should include a capturing group for the value.
        """
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE) if pattern else None
    
    def extract(self, text: str) -> Optional[AttributeNode]:
        """
        Extract an attribute and its values from text.
        
        Args:
            text: The text to extract from.
            
        Returns:
            Attribute node if found, None otherwise.
        """
        if not self.pattern:
            logger.debug(f"No pattern defined for attribute {self.name}")
            return None
            
        match = self.pattern.search(text)
        
        if not match or not match.lastindex:
            logger.debug(f"No match found for attribute {self.name} in text: {text[:50]}...")
            return None
            
        value_text = match.group(1).strip()
        
        if not value_text:
            logger.debug(f"Empty value for attribute {self.name}")
            return None
            
        logger.debug(f"Found value for attribute {self.name}: {value_text}")
        values = self._parse_values(value_text)
        
        return AttributeNode(self.name, values=values)
    
    def _parse_values(self, text: str) -> List[AttributeValue]:
        """
        Parse attribute values from text, handling ranges, units, etc.
        
        Args:
            text: The value text to parse.
            
        Returns:
            List of parsed attribute values.
        """
        # Basic implementation - can be enhanced based on specific needs
        values = []
        
        # Handle ranges with dashes (e.g., "8--25 dm")
        range_match = re.match(r'(\d+(?:\.\d+)?)\s*--\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?', text)
        
        if range_match:
            start_val, end_val, unit = range_match.groups()
            values.append(AttributeValue(start_val, unit=unit, is_range_start=True))
            values.append(AttributeValue(end_val, unit=unit, is_range_end=True))
            return values
            
        # Handle OR values (e.g., "shrub or thicket-forming")
        if ' or ' in text:
            or_parts = [part.strip() for part in text.split(' or ')]
            
            for part in or_parts:
                values.append(AttributeValue(part))
                
            return values
            
        # Handle simple value with unit (e.g., "5 mm")
        unit_match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', text)
        
        if unit_match:
            val, unit = unit_match.groups()
            values.append(AttributeValue(val, unit=unit))
            return values
            
        # Default: treat as a simple value
        values.append(AttributeValue(text))
        return values
