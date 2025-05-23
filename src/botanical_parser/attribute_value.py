"""
Attribute value class representing specific values of botanical attributes.
"""
from typing import Dict, Optional


class AttributeValue:
    """
    Represents a specific value for an attribute, with support for ranges, units, etc.
    """
    
    def __init__(self, raw_value: str, unit: Optional[str] = None, 
                 is_range_start: bool = False, is_range_end: bool = False):
        """
        Initialize an attribute value.
        
        Args:
            raw_value: The raw value string.
            unit: Optional unit for this value (e.g., "mm", "cm").
            is_range_start: Whether this value is the start of a range.
            is_range_end: Whether this value is the end of a range.
        """
        self.raw_value = raw_value
        self.unit = unit
        self.is_range_start = is_range_start
        self.is_range_end = is_range_end
    
    def __eq__(self, other):
        """
        Compare two AttributeValue objects for equality.
        """
        if not isinstance(other, AttributeValue):
            return NotImplemented
        return (
            self.raw_value == other.raw_value and
            self.unit == other.unit and
            self.is_range_start == other.is_range_start and
            self.is_range_end == other.is_range_end
        )
    
    def to_dict(self) -> Dict:
        """
        Convert attribute value to dictionary representation.
        
        Returns:
            Dictionary representation of the attribute value.
        """
        return {
            'raw_value': self.raw_value,
            'unit': self.unit,
            'is_range_start': self.is_range_start,
            'is_range_end': self.is_range_end
        }
    
    def __repr__(self) -> str:
        """
        String representation of the attribute value.
        
        Returns:
            String representation.
        """
        parts = [f"raw_value='{self.raw_value}'"]
        
        if self.unit:
            parts.append(f"unit='{self.unit}'")
            
        if self.is_range_start:
            parts.append("is_range_start=True")
            
        if self.is_range_end:
            parts.append("is_range_end=True")
            
        return f"AttributeValue({', '.join(parts)})"
