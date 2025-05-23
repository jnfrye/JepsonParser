"""
Attribute extractor classes for extracting attributes from botanical descriptions.
Uses the Template Method pattern with specialized extractors for different attribute types.
"""
import re
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Pattern
from .attribute_node import AttributeNode
from .attribute_value import AttributeValue

# Configure logging
logger = logging.getLogger(__name__)


class AttributeExtractor(ABC):
    """
    Abstract base class for extracting botanical attributes from text.
    Implements the Template Method pattern.
    """
    
    def __init__(self, name: str):
        """
        Initialize an attribute extractor.
        
        Args:
            name: The name of the attribute to extract.
        """
        self.name = name
        self.pattern = re.compile(self.generate_pattern(), re.IGNORECASE)
    
    @abstractmethod
    def generate_pattern(self) -> str:
        """
        Generate the regex pattern for matching this attribute.
        To be implemented by subclasses.
        
        Returns:
            Regex pattern string
        """
        pass
        
    @abstractmethod
    def parse_values(self, text: str) -> List[AttributeValue]:
        """
        Parse attribute values from text, handling specific formats.
        To be implemented by subclasses.
        
        Args:
            text: The value text to parse.
            
        Returns:
            List of parsed attribute values.
        """
        pass
    
    def extract(self, text: str) -> Optional[AttributeNode]:
        """
        Extract an attribute and its values from text.
        Template method that orchestrates the extraction process.
        
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
        values = self.parse_values(value_text)
        
        return AttributeNode(self.name, values=values)


class NumericAttributeExtractor(AttributeExtractor):
    """
    Extracts numeric attributes with units and ranges.
    Specialized for measurements, dimensions, and numeric ranges.
    """
    
    def __init__(self, name: str, 
                 prefix_qualifiers: Optional[List[str]] = None,
                 allow_decimal: bool = True,
                 units: Optional[List[str]] = None):
        """
        Initialize a numeric attribute extractor.
        
        Args:
            name: The name of the attribute to extract.
            prefix_qualifiers: Optional list of qualifier words that may precede the range
            allow_decimal: Whether to allow decimal numbers
            units: Optional list of unit words that may follow the range
        """
        self.prefix_qualifiers = prefix_qualifiers or [
            "generally", "mostly", "usually", "approximately", 
            "ca", "ca.", "about", "up to", "to"
        ]
        self.allow_decimal = allow_decimal
        self.units = units or ["mm", "cm", "m", "dm"]
        super().__init__(name)
    
    def generate_pattern(self) -> str:
        """
        Generate regex for numeric values and ranges.
        
        Returns:
            A regex pattern string for matching numeric ranges and single values with units.
        """
        # Build the qualifier pattern - optional qualifier at start
        qualifier_pattern = r"(?:{})\s+".format("|".join(self.prefix_qualifiers)) if self.prefix_qualifiers else ""
        
        # Build the number pattern based on whether decimals are allowed
        if self.allow_decimal:
            number_pattern = r"(\d+(?:\.\d+)?)"
        else:
            number_pattern = r"(\d+)"
        
        # Build the parenthetical pattern - always allow parenthetical values
        parenthetical_pattern = r"(?:\((\d+(?:\.\d+)?)\))?"
        
        # Build the units pattern
        units_pattern = r"(?:\s*(?:{}))?" .format("|".join(self.units)) if self.units else ""
        
        # Pattern for ranges: optional qualifier + first number + -- + second number + optional parenthetical + optional units
        range_pattern = r"(?:{})?{}--{}{}{}".format(
            qualifier_pattern, 
            number_pattern, 
            number_pattern,
            parenthetical_pattern, 
            units_pattern
        )
        
        # Pattern for simple values with units: optional qualifier + number + optional units
        simple_pattern = r"(?:{})?{}\s*(?:{})".format(
            qualifier_pattern,
            number_pattern,
            "|".join(self.units)
        ) if self.units else ""
        
        # Combine both patterns
        if simple_pattern:
            combined_pattern = f"{range_pattern}|{simple_pattern}"
        else:
            combined_pattern = range_pattern
            
        return r"({})".format(combined_pattern)
    
    def parse_values(self, text: str) -> List[AttributeValue]:
        """
        Parse numeric ranges into structured values.
        
        Args:
            text: The value text to parse.
            
        Returns:
            List of parsed attribute values.
        """
        values = []
        
        # Handle ranges with dashes (e.g., "8--25 dm")
        range_match = re.match(r'(\d+(?:\.\d+)?)\s*--\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?', text)
        
        if range_match:
            start_val, end_val, unit = range_match.groups()
            values.append(AttributeValue(start_val, unit=unit, is_range_start=True))
            values.append(AttributeValue(end_val, unit=unit, is_range_end=True))
            return values
        
        # Check for parenthetical max values (e.g., "10(15) cm")
        parenthetical_match = re.match(r'(\d+(?:\.\d+)?)\s*\((\d+(?:\.\d+)?)\)\s*([a-zA-Z]+)?', text)
        if parenthetical_match:
            typical_val, max_val, unit = parenthetical_match.groups()
            values.append(AttributeValue(typical_val, unit=unit))
            values.append(AttributeValue(max_val, unit=unit, is_range_end=True))
            return values
        
        # Handle simple value with unit (e.g., "5 mm")
        unit_match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', text)
        
        if unit_match:
            val, unit = unit_match.groups()
            values.append(AttributeValue(val, unit=unit))
            return values
            
        # Default: treat as a simple numeric value
        values.append(AttributeValue(text))
        return values


class QualitativeAttributeExtractor(AttributeExtractor):
    """
    Extracts qualitative descriptive attributes.
    Specialized for descriptive terms like colors, shapes, textures, etc.
    """
    
    def __init__(self, name: str, 
                 value_words: List[str],
                 qualifiers: Optional[List[str]] = None,
                 conjunctions: Optional[List[str]] = None):
        """
        Initialize a qualitative attribute extractor.
        
        Args:
            name: The name of the attribute to extract.
            value_words: List of specific value words to match (e.g., "curved", "hairy")
            qualifiers: Optional list of qualifier words/symbols
            conjunctions: Optional list of conjunction words
        """
        self.value_words = value_words
        self.qualifiers = qualifiers or [
            "generally", "mostly", "sometimes", "rarely", "often", 
            "usually", "primarily", "mainly", "sparsely", "densely", 
            "highly", "slightly", "moderately", "\\+-", "few", "many",
            "several", "numerous", "occasional", "frequent", "abundant",
            "sparse", "dense", "thick"
        ]
        self.conjunctions = conjunctions or [
            "and", "or", "to", "through", "with", "without"
        ]
        super().__init__(name)
    
    def generate_pattern(self) -> str:
        """
        Generate regex for qualitative descriptions.
        
        Returns:
            A regex pattern string for matching qualitative descriptions.
        """
        # Build the qualifier pattern - optional qualifier at start or after conjunction
        qualifier_pattern = r"(?:{})".format("|".join(self.qualifiers)) if self.qualifiers else ""
        
        # Build the conjunction pattern - optional conjunction between value words
        conjunction_pattern = r"(?:\s+(?:{})\s+)".format("|".join(self.conjunctions)) if self.conjunctions else ""
        
        # Build the value word pattern
        value_word_pattern = r"(?:{})".format("|".join(self.value_words))
        
        # Start with optional qualifier followed by a value word
        pattern = r"(?:{}(?:\s+))?{}".format(qualifier_pattern, value_word_pattern)
        
        # Add ability to have repeating conjunction + optional qualifier + value word combinations
        pattern += r"(?:{}(?:{}(?:\s+))?{})*(\.)?".format(
            conjunction_pattern, qualifier_pattern, value_word_pattern
        )
        
        return r"({})".format(pattern)
    
    def parse_values(self, text: str) -> List[AttributeValue]:
        """
        Parse qualitative descriptions into structured values.
        
        Args:
            text: The value text to parse.
            
        Returns:
            List of parsed attribute values.
        """
        values = []
        
        # Handle all supported conjunctions
        for conjunction in self.conjunctions:
            conj_pattern = f" {conjunction} "
            if conj_pattern in text:
                parts = [part.strip() for part in text.split(conj_pattern)]
                for part in parts:
                    values.append(AttributeValue(part))
                return values
        
        # Default: treat as a simple qualitative value
        values.append(AttributeValue(text))
        return values


# Legacy constructor for backward compatibility
def create_attribute_extractor(name: str, pattern: str) -> AttributeExtractor:
    """
    Create an attribute extractor with a custom pattern (for backward compatibility).
    
    Args:
        name: The name of the attribute.
        pattern: The regex pattern to use.
        
    Returns:
        An AttributeExtractor instance.
    """
    class CustomAttributeExtractor(AttributeExtractor):
        def generate_pattern(self) -> str:
            return pattern
            
        def parse_values(self, text: str) -> List[AttributeValue]:
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
    
    return CustomAttributeExtractor(name)
