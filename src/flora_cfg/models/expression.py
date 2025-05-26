"""
Expression models for representing parsed botanical expressions.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional, Any

class BotanicalExpression(ABC):
    """Abstract base class for all botanical expressions."""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the expression to a dictionary representation."""
        pass

class ValueExpression(BotanicalExpression):
    """A simple value expression, such as a word or number."""
    
    def __init__(self, value: Any, value_type: str = "word"):
        """
        Initialize a value expression.
        
        Args:
            value: The value (word, number, etc.)
            value_type: The type of value ("word", "number", etc.)
        """
        self.value = value
        self.value_type = value_type
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": "value",
            "value_type": self.value_type,
            "value": self.value
        }
    
    def __str__(self) -> str:
        return f"{self.value}"

class QualifierExpression(BotanicalExpression):
    """A qualifier applied to another expression."""
    
    def __init__(self, qualifier: str, expression: BotanicalExpression, qualifier_type: str = "adjacent"):
        """
        Initialize a qualifier expression.
        
        Args:
            qualifier: The qualifier text (e.g., "sparsely", "generally")
            expression: The expression being qualified
            qualifier_type: Type of qualifier ("adjacent", "collective", "distributive")
        """
        self.qualifier = qualifier
        self.expression = expression
        self.qualifier_type = qualifier_type
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": "qualifier",
            "qualifier_type": self.qualifier_type,
            "qualifier": self.qualifier,
            "expression": self.expression.to_dict()
        }
    
    def __str__(self) -> str:
        return f"{self.qualifier} {self.expression}"

class ConjunctionExpression(BotanicalExpression):
    """A conjunction of multiple expressions (e.g., "A or B", "X to Y")."""
    
    def __init__(self, conjunction: str, expressions: List[BotanicalExpression]):
        """
        Initialize a conjunction expression.
        
        Args:
            conjunction: The conjunction text (e.g., "or", "and", "to")
            expressions: The list of joined expressions
        """
        self.conjunction = conjunction
        self.expressions = expressions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": "conjunction",
            "conjunction": self.conjunction,
            "expressions": [expr.to_dict() for expr in self.expressions]
        }
    
    def __str__(self) -> str:
        expr_strs = [str(expr) for expr in self.expressions]
        return f" {self.conjunction} ".join(expr_strs)

class RangeExpression(BotanicalExpression):
    """A range expression (e.g., "1--5 mm")."""
    
    def __init__(self, 
                 start: BotanicalExpression, 
                 end: BotanicalExpression, 
                 unit: Optional[str] = None):
        """
        Initialize a range expression.
        
        Args:
            start: The start of the range
            end: The end of the range
            unit: Optional unit for the range
        """
        self.start = start
        self.end = end
        self.unit = unit
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "type": "range",
            "start": self.start.to_dict(),
            "end": self.end.to_dict()
        }
        
        if self.unit:
            result["unit"] = self.unit
            
        return result
    
    def __str__(self) -> str:
        unit_str = f" {self.unit}" if self.unit else ""
        return f"{self.start}--{self.end}{unit_str}"
