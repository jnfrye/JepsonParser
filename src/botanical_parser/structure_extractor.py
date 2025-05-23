"""
Structure extractor class for extracting botanical structures from descriptions.
"""
import re
import logging
from typing import List, Optional, Dict, Pattern, Tuple
from .structure_node import StructureNode
from .attribute_node import AttributeNode
from .attribute_extractor import AttributeExtractor

# Configure logging
logger = logging.getLogger(__name__)


class StructureExtractor:
    """
    Extracts botanical structures from text.
    
    A structure extractor can have child structure extractors and attribute extractors.
    It recursively builds a tree of StructureNodes by first extracting child structures,
    then extracting attributes from the remaining text.
    """
    
    def __init__(self, name: str, pattern: Optional[str] = None, 
                 attribute_extractors: Optional[List[AttributeExtractor]] = None,
                 child_extractors: Optional[List['StructureExtractor']] = None):
        """
        Initialize a structure extractor.
        
        Args:
            name: The name of the structure to extract.
            pattern: Regular expression pattern to match the structure.
                     Should include a capturing group for the content.
            attribute_extractors: List of attribute extractors for this structure.
            child_extractors: List of child structure extractors.
        """
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE | re.DOTALL) if pattern else None
        self.attribute_extractors = attribute_extractors or []
        self.child_extractors = child_extractors or []
    
    def extract(self, text: str) -> Optional[StructureNode]:
        """
        Extract a structure node and all its components from text.
        
        Args:
            text: The text to extract from.
            
        Returns:
            Structure node if found, None otherwise.
        """
        # Special case for root-level extractor (no pattern)
        if not self.pattern:
            logger.debug(f"Processing root level extractor {self.name}")
            root_node = StructureNode(self.name)
            
            # Extract all child structures
            for child_extractor in self.child_extractors:
                child_node = child_extractor.extract(text)
                if child_node:
                    logger.debug(f"Adding child {child_node.name} to root {self.name}")
                    root_node.add_child(child_node)
                    
            return root_node
        
        # Regular structure extractor with pattern
        structure_match = self.pattern.search(text)
        
        if not structure_match:
            logger.debug(f"No match found for structure {self.name} in text: {text[:50]}...")
            return None
            
        # Create structure node and extract matched content
        structure_text = structure_match.group(1) if structure_match.lastindex else ""
        
        if not structure_text.strip():
            logger.debug(f"Empty content for structure {self.name}")
            return None
            
        logger.debug(f"Found content for structure {self.name}: {structure_text[:50]}...")
        structure_node = StructureNode(self.name)
        
        # Extract child structures first
        remaining_text = structure_text
        child_regions = self._extract_child_regions(structure_text)
        
        for region in child_regions:
            child_node = region['extractor'].extract(region['text'])
            if child_node:
                logger.debug(f"Adding child {child_node.name} to {self.name}")
                structure_node.add_child(child_node)
                # Remove the matched text from remaining_text to avoid double parsing
                remaining_text = remaining_text.replace(region['text'], ' ' * len(region['text']))
        
        # Extract attributes from remaining text
        for attr_extractor in self.attribute_extractors:
            attr_node = attr_extractor.extract(remaining_text)
            if attr_node:
                logger.debug(f"Adding attribute {attr_node.name} to {self.name}")
                structure_node.add_attribute(attr_node)
                
        return structure_node
    
    def _extract_child_regions(self, text: str) -> List[Dict]:
        """
        Find regions of text that match child structure extractors.
        
        Args:
            text: The text to analyze.
            
        Returns:
            List of dictionaries containing extractor, text, and span information.
        """
        regions = []
        
        for extractor in self.child_extractors:
            if not extractor.pattern:
                continue
                
            for match in extractor.pattern.finditer(text):
                if not match.lastindex:
                    continue
                    
                start, end = match.span(0)  # Use full match span
                regions.append({
                    'extractor': extractor,
                    'text': text[start:end],
                    'start': start,
                    'end': end
                })
        
        # Sort regions by start position
        regions.sort(key=lambda r: r['start'])
        
        # Handle overlapping regions by adjusting end positions
        for i in range(len(regions) - 1):
            if regions[i]['end'] > regions[i + 1]['start']:
                regions[i]['end'] = regions[i + 1]['start']
                regions[i]['text'] = text[regions[i]['start']:regions[i]['end']]
                
        return regions
