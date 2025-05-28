"""
Tests for the modular function-based grammar components.
"""
import pytest
from nltk.parse.recursivedescent import RecursiveDescentParser
from nltk.grammar import CFG

from src.flora_cfg.grammar.core import GrammarBuilder
from src.flora_cfg.grammar.components import (
    add_number_grammar,
    add_basic_terms_grammar,
    add_unit_grammar,
    add_adjacent_qualifier_grammar,
    add_collective_qualifier_grammar,
    add_conjunction_grammar,
    add_qualified_conjunction_grammar,
    add_value_grammar,
    build_jepson_grammar
)

class TestGrammarComponents:
    
    def test_number_grammar(self):
        """Test the number grammar component."""
        builder = GrammarBuilder(start_symbol="VALUE")
        builder = add_number_grammar(builder, max_number=10)
        
        grammar = builder.build()
        parser = RecursiveDescentParser(grammar)
        
        # Test parsing numbers
        trees = list(parser.parse(["5"]))
        assert len(trees) > 0
        
        # This should fail (not in grammar)
        with pytest.raises(ValueError):
            list(parser.parse(["11"]))
    
    def test_basic_terms_grammar(self):
        """Test the basic terms grammar component."""
        builder = GrammarBuilder(start_symbol="VALUE")
        builder = add_basic_terms_grammar(builder, growth_forms=["herb", "shrub"])
        
        grammar = builder.build()
        parser = RecursiveDescentParser(grammar)
        
        # Test parsing basic terms
        trees = list(parser.parse(["herb"]))
        assert len(trees) > 0
        
        # This should fail (not in grammar)
        with pytest.raises(ValueError):
            list(parser.parse(["tree"]))
    
    def test_composite_grammar(self):
        """Test combining multiple grammar components."""
        builder = GrammarBuilder(start_symbol="VALUE")
        builder = add_number_grammar(builder, max_number=10)
        builder = add_basic_terms_grammar(builder, growth_forms=["herb", "shrub"])
        builder = add_adjacent_qualifier_grammar(builder, qualifiers=["sparsely", "densely"])
        
        grammar = builder.build()
        parser = RecursiveDescentParser(grammar)
        
        # Test parsing a qualified term
        trees = list(parser.parse(["sparsely", "herb"]))
        assert len(trees) > 0
        
        # Test parsing basic terms
        trees = list(parser.parse(["herb"]))
        assert len(trees) > 0
        
        # Test parsing numbers
        trees = list(parser.parse(["5"]))
        assert len(trees) > 0
    
    def test_conjunction_grammar(self):
        """Test the conjunction grammar component."""
        builder = GrammarBuilder(start_symbol="VALUE")
        builder = add_number_grammar(builder, max_number=10)
        builder = add_basic_terms_grammar(builder, growth_forms=["herb", "shrub"])
        builder = add_adjacent_qualifier_grammar(builder, qualifiers=["sparsely", "densely"])
        builder = add_conjunction_grammar(builder, conjunctions=["or", "and"])
        
        grammar = builder.build()
        parser = RecursiveDescentParser(grammar)
        
        # Test parsing a conjunction
        trees = list(parser.parse(["herb", "or", "shrub"]))
        assert len(trees) > 0
        
        # Test parsing a qualified conjunction
        trees = list(parser.parse(["sparsely", "herb", "or", "shrub"]))
        assert len(trees) > 0
    
    def test_build_jepson_grammar(self):
        """Test the complete Jepson grammar builder."""
        grammar = build_jepson_grammar(max_number=10)
        parser = RecursiveDescentParser(grammar)
        
        # Test simple values
        assert len(list(parser.parse(["herb"]))) > 0
        assert len(list(parser.parse(["5"]))) > 0
        
        # Test qualified values
        assert len(list(parser.parse(["sparsely", "herb"]))) > 0
        assert len(list(parser.parse(["generally", "herb"]))) > 0
        
        # Test conjunctions
        assert len(list(parser.parse(["herb", "or", "shrub"]))) > 0
        assert len(list(parser.parse(["herb", "and", "shrub"]))) > 0
        
        # Test complex expressions
        assert len(list(parser.parse(["generally", "sparsely", "herb"]))) > 0
        assert len(list(parser.parse(["herb", "or", "generally", "shrub"]))) > 0
        
    def test_grammar_ambiguity(self):
        """Test for grammar ambiguity (informational, not failure)."""
        grammar = build_jepson_grammar(max_number=10)
        parser = RecursiveDescentParser(grammar)
        
        # Check basic tokens for ambiguity
        trees = list(parser.parse(["herb"]))
        if len(trees) > 1:
            print(f"Note: Grammar is ambiguous - 'herb' has {len(trees)} parse trees")
            
        # It's okay to have multiple parse trees, we just need to be aware of it
        # This test doesn't assert anything, it's just informative
