"""
Grammar definitions for basic botanical values.
"""
from typing import List, Optional
from src.flora_cfg.grammar.core import GrammarBuilder, CFG

# Common botanical terms for our initial grammar
GROWTH_FORMS = ["herb", "shrub", "tree", "vine", "subshrub", "annual", "perennial"]

SURFACE_TERMS = [
    "glabrous", "hairy", "pubescent", "tomentose", "hirsute", "pilose", 
    "villous", "scabrous", "glandular", "smooth", "rough"
]

ADJACENT_QUALIFIERS = [
    "sparsely", "densely", "finely", "coarsely", "slightly", "heavily", 
    "minutely", "distinctly", "moderately", "strongly"
]

COLLECTIVE_QUALIFIERS = [
    "generally", "usually", "sometimes", "rarely", "often", "mostly", 
    "occasionally", "typically", "mainly", "predominantly"
]

UNITS = ["mm", "cm", "m", "dm"]

CONJUNCTIONS = ["and", "or", "to", "--"]

def build_value_grammar() -> CFG:
    """
    Build a grammar for parsing botanical values.
    
    Returns:
        A context-free grammar for botanical values
    """
    builder = GrammarBuilder(start_symbol="VALUE")
    
    # Simple terms
    builder.add_values("GROWTH_FORM", GROWTH_FORMS)
    builder.add_values("SURFACE", SURFACE_TERMS)
    builder.add_values("UNIT", UNITS)
    builder.add_values("ADJ_QUALIFIER", ADJACENT_QUALIFIERS)
    builder.add_values("COLL_QUALIFIER", COLLECTIVE_QUALIFIERS)
    builder.add_values("CONJUNCTION", CONJUNCTIONS)
    
    # Value expressions
    builder.add_rule("VALUE", ["SIMPLE_VALUE"])
    builder.add_rule("VALUE", ["QUALIFIED_VALUE"])
    builder.add_rule("VALUE", ["CONJUNCTION_VALUE"])
    builder.add_rule("VALUE", ["UNIT_VALUE"])
    builder.add_rule("VALUE", ["QUALIFIED_CONJUNCTION"])

    # Simple values
    builder.add_rule("SIMPLE_VALUE", ["GROWTH_FORM"])
    builder.add_rule("SIMPLE_VALUE", ["SURFACE"])
    builder.add_rule("SIMPLE_VALUE", ["NUMBER"])
    
    # Numbers
    for i in range(1, 100):
        builder.add_terminal_rule("NUMBER", str(i))
    
    # Qualified values
    builder.add_rule("QUALIFIED_VALUE", ["ADJ_QUALIFIER", "SIMPLE_VALUE"])
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "SIMPLE_VALUE"])
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "QUALIFIED_VALUE"])
    
    # Unit expressions
    builder.add_rule("UNIT_VALUE", ["NUMBER", "UNIT"])
    builder.add_rule("UNIT_VALUE", ["QUALIFIED_NUMBER", "UNIT"])
    builder.add_rule("QUALIFIED_NUMBER", ["ADJ_QUALIFIER", "NUMBER"])
    
    # Conjunction expressions
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    
    # Qualified conjunctions (with collective qualifiers)
    builder.add_rule("QUALIFIED_CONJUNCTION", ["COLL_QUALIFIER", "CONJUNCTION_VALUE"])
    
    # Unit application to conjunctions (e.g., "5 or 10 mm")
    builder.add_rule("UNIT_VALUE", ["CONJUNCTION_VALUE", "UNIT"])
    
    return builder.build()

def build_value_grammar_with_scope(
    growth_forms: Optional[List[str]] = None,
    surface_terms: Optional[List[str]] = None,
    adjacent_qualifiers: Optional[List[str]] = None,
    collective_qualifiers: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    conjunctions: Optional[List[str]] = None
) -> CFG:
    """
    Build a grammar for parsing botanical values with custom vocabulary.
    
    Args:
        growth_forms: List of growth form terms
        surface_terms: List of surface description terms
        adjacent_qualifiers: List of adjacent qualifiers
        collective_qualifiers: List of collective qualifiers
        units: List of measurement units
        conjunctions: List of conjunctions
        
    Returns:
        A context-free grammar for botanical values
    """
    builder = GrammarBuilder(start_symbol="VALUE")
    
    # Use provided lists or defaults
    growth_forms = growth_forms or GROWTH_FORMS
    surface_terms = surface_terms or SURFACE_TERMS
    adjacent_qualifiers = adjacent_qualifiers or ADJACENT_QUALIFIERS
    collective_qualifiers = collective_qualifiers or COLLECTIVE_QUALIFIERS
    units = units or UNITS
    conjunctions = conjunctions or CONJUNCTIONS
    
    # Simple terms
    builder.add_values("GROWTH_FORM", growth_forms)
    builder.add_values("SURFACE", surface_terms)
    builder.add_values("UNIT", units)
    builder.add_values("ADJ_QUALIFIER", adjacent_qualifiers)
    builder.add_values("COLL_QUALIFIER", collective_qualifiers)
    builder.add_values("CONJUNCTION", conjunctions)
    
    # Value expressions
    builder.add_rule("VALUE", ["SIMPLE_VALUE"])
    builder.add_rule("VALUE", ["QUALIFIED_VALUE"])
    builder.add_rule("VALUE", ["CONJUNCTION_VALUE"])
    builder.add_rule("VALUE", ["UNIT_VALUE"])
    builder.add_rule("VALUE", ["QUALIFIED_CONJUNCTION"])
    
    # Simple values
    builder.add_rule("SIMPLE_VALUE", ["GROWTH_FORM"])
    builder.add_rule("SIMPLE_VALUE", ["SURFACE"])
    builder.add_rule("SIMPLE_VALUE", ["NUMBER"])
    
    # Numbers
    for i in range(1, 100):
        builder.add_terminal_rule("NUMBER", str(i))
    
    # Qualified values
    builder.add_rule("QUALIFIED_VALUE", ["ADJ_QUALIFIER", "SIMPLE_VALUE"])
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "SIMPLE_VALUE"])
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "QUALIFIED_VALUE"])
    
    # Unit expressions
    builder.add_rule("UNIT_VALUE", ["NUMBER", "UNIT"])
    builder.add_rule("UNIT_VALUE", ["QUALIFIED_NUMBER", "UNIT"])
    builder.add_rule("QUALIFIED_NUMBER", ["ADJ_QUALIFIER", "NUMBER"])
 
    # Qualified conjunctions (with collective qualifiers)
    builder.add_rule("QUALIFIED_CONJUNCTION", ["COLL_QUALIFIER", "CONJUNCTION_VALUE"])
    
    # Unit application to conjunctions (e.g., "5 or 10 mm")
    builder.add_rule("UNIT_VALUE", ["CONJUNCTION_VALUE", "UNIT"])
    
    # Conjunction expressions
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    
    return builder.build()
