"""
Tests for the botanical value parser.
"""
import pytest
from src.flora_cfg.parsers.value_parser import BotanicalValueParser
from src.flora_cfg.models.expression import (
    ValueExpression, 
    QualifierExpression, 
    ConjunctionExpression,
    RangeExpression
)

class TestBotanicalValueParser:
    """Test cases for the BotanicalValueParser class."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance for tests."""
        return BotanicalValueParser()
    
    def test_simple_values(self, parser):
        """Test parsing of simple values."""
        # Test simple word values
        result = parser.parse("hairy")
        assert isinstance(result, ValueExpression)
        assert result.value == "hairy"
        assert result.value_type == "word"
        
        result = parser.parse("shrub")
        assert isinstance(result, ValueExpression)
        assert result.value == "shrub"
        assert result.value_type == "word"
        
        # Test numeric values
        result = parser.parse("5")
        assert isinstance(result, ValueExpression)
        assert result.value == 5
        assert result.value_type == "number"
    
    def test_adjacent_qualifiers(self, parser):
        """Test parsing of adjacent qualifiers."""
        result = parser.parse("sparsely hairy")
        
        assert isinstance(result, QualifierExpression)
        assert result.qualifier == "sparsely"
        assert result.qualifier_type == "adjacent"
        
        assert isinstance(result.expression, ValueExpression)
        assert result.expression.value == "hairy"
    
    def test_collective_qualifiers(self, parser):
        """Test parsing of collective qualifiers."""
        result = parser.parse("generally hairy")
        
        assert isinstance(result, QualifierExpression)
        assert result.qualifier == "generally"
        assert result.qualifier_type == "collective"
        
        assert isinstance(result.expression, ValueExpression)
        assert result.expression.value == "hairy"
    
    def test_nested_qualifiers(self, parser):
        """Test parsing of nested qualifiers."""
        result = parser.parse("generally sparsely hairy")
        
        assert isinstance(result, QualifierExpression)
        assert result.qualifier == "generally"
        assert result.qualifier_type == "collective"
        
        assert isinstance(result.expression, QualifierExpression)
        assert result.expression.qualifier == "sparsely"
        assert result.expression.qualifier_type == "adjacent"
        
        assert isinstance(result.expression.expression, ValueExpression)
        assert result.expression.expression.value == "hairy"
    
    def test_conjunctions(self, parser):
        """Test parsing of conjunctions."""
        result = parser.parse("glabrous or hairy")
        
        assert isinstance(result, ConjunctionExpression)
        assert result.conjunction == "or"
        assert len(result.expressions) == 2
        
        assert isinstance(result.expressions[0], ValueExpression)
        assert result.expressions[0].value == "glabrous"
        
        assert isinstance(result.expressions[1], ValueExpression)
        assert result.expressions[1].value == "hairy"
    
    def test_qualified_conjunctions(self, parser):
        """Test parsing of qualified conjunctions."""
        result = parser.parse("sparsely hairy or densely pubescent")
        
        assert isinstance(result, ConjunctionExpression)
        assert result.conjunction == "or"
        assert len(result.expressions) == 2
        
        assert isinstance(result.expressions[0], QualifierExpression)
        assert result.expressions[0].qualifier == "sparsely"
        assert result.expressions[0].expression.value == "hairy"
        
        assert isinstance(result.expressions[1], QualifierExpression)
        assert result.expressions[1].qualifier == "densely"
        assert result.expressions[1].expression.value == "pubescent"
    
    def test_ranges(self, parser):
        """Test parsing of ranges."""
        result = parser.parse("1 -- 5")
        
        assert isinstance(result, RangeExpression)
        assert result.start.value == 1
        assert result.end.value == 5
        
        # Test with "to" instead of "--"
        result = parser.parse("1 to 5")
        
        assert isinstance(result, RangeExpression)
        assert result.start.value == 1
        assert result.end.value == 5
    
    def test_unit_values(self, parser):
        """Test parsing values with units."""
        # For now, units are handled as qualifiers
        result = parser.parse("5 mm")
        
        assert isinstance(result, QualifierExpression)
        assert result.qualifier == "mm"
        assert result.qualifier_type == "unit"
        
        assert isinstance(result.expression, ValueExpression)
        assert result.expression.value == 5
    
    def test_complex_expressions(self, parser):
        """Test parsing of more complex expressions."""
        result = parser.parse("generally glabrous to sparsely hairy")
    
        # The expression should be a QualifierExpression with "generally" as the qualifier
        # for the entire "glabrous to sparsely hairy" expression
        assert isinstance(result, QualifierExpression)
        assert result.qualifier == "generally"
        assert result.qualifier_type == "collective"
        
        # The inner expression should be a ConjunctionExpression with "to" as the conjunction
        inner = result.expression
        assert isinstance(inner, ConjunctionExpression)
        assert inner.conjunction == "to"
        
        # Check left side (glabrous)
        left = inner.expressions[0]
        assert isinstance(left, ValueExpression)
        assert left.value == "glabrous"
        
        # Check right side (sparsely hairy)
        right = inner.expressions[1]
        assert isinstance(right, QualifierExpression)
        assert right.qualifier == "sparsely"
        assert isinstance(right.expression, ValueExpression)
        assert right.expression.value == "hairy"
