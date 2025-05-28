"""
Modular grammar components for botanical value parsing.
"""
from typing import List, Optional
from src.flora_cfg.grammar.core import GrammarBuilder, CFG

# Common botanical terms
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

def add_number_grammar(builder: GrammarBuilder, max_number: int = 100) -> GrammarBuilder:
    """
    Add grammar rules for numeric values.
    
    Args:
        builder: The grammar builder to add rules to
        max_number: The maximum number to include
        
    Returns:
        The updated grammar builder
    """
    # Add number terminals
    for i in range(1, max_number + 1):
        builder.add_terminal_rule("NUMBER", str(i))
    
    # Register numbers as simple values
    builder.add_rule("SIMPLE_VALUE", ["NUMBER"])
    
    # Make them valid values
    builder.add_rule("VALUE", ["SIMPLE_VALUE"])
    
    return builder

def add_basic_terms_grammar(
    builder: GrammarBuilder,
    growth_forms: Optional[List[str]] = None,
    surface_terms: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for basic botanical terms.
    
    Args:
        builder: The grammar builder to add rules to
        growth_forms: Optional list of growth form terms (e.g., "herb", "shrub")
        surface_terms: Optional list of surface terms (e.g., "glabrous", "hairy")
        
    Returns:
        The updated grammar builder
    """
    # Use provided lists or defaults
    growth_forms = growth_forms or GROWTH_FORMS
    surface_terms = surface_terms or SURFACE_TERMS
    
    # Add basic terms
    builder.add_values("GROWTH_FORM", growth_forms)
    builder.add_values("SURFACE", surface_terms)
    
    # Register as simple values
    builder.add_rule("SIMPLE_VALUE", ["GROWTH_FORM"])
    builder.add_rule("SIMPLE_VALUE", ["SURFACE"])
    
    # Make them valid values
    builder.add_rule("VALUE", ["SIMPLE_VALUE"])
    
    return builder

def add_unit_grammar(
    builder: GrammarBuilder,
    units: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for units of measurement.
    
    Args:
        builder: The grammar builder to add rules to
        units: Optional list of unit terms (e.g., "mm", "cm")
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    units = units or UNITS
    
    # Add unit terms
    builder.add_values("UNIT", units)
    
    # Add unit expressions
    builder.add_rule("UNIT_VALUE", ["NUMBER", "UNIT"])
    builder.add_rule("UNIT_VALUE", ["QUALIFIED_NUMBER", "UNIT"])
    builder.add_rule("QUALIFIED_NUMBER", ["ADJ_QUALIFIER", "NUMBER"])
    
    # Make them valid values
    builder.add_rule("VALUE", ["UNIT_VALUE"])
    
    return builder

def add_adjacent_qualifier_grammar(
    builder: GrammarBuilder,
    qualifiers: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for adjacent qualifiers.
    
    Args:
        builder: The grammar builder to add rules to
        qualifiers: Optional list of adjacent qualifier terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    qualifiers = qualifiers or ADJACENT_QUALIFIERS
    
    # Add qualifier terms
    builder.add_values("ADJ_QUALIFIER", qualifiers)
    
    # Add qualifier expressions
    builder.add_rule("QUALIFIED_VALUE", ["ADJ_QUALIFIER", "SIMPLE_VALUE"])
    
    # Make them valid values
    builder.add_rule("VALUE", ["QUALIFIED_VALUE"])
    
    return builder

def add_collective_qualifier_grammar(
    builder: GrammarBuilder,
    qualifiers: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for collective qualifiers.
    
    Args:
        builder: The grammar builder to add rules to
        qualifiers: Optional list of collective qualifier terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    qualifiers = qualifiers or COLLECTIVE_QUALIFIERS
    
    # Add qualifier terms
    builder.add_values("COLL_QUALIFIER", qualifiers)
    
    # Add qualifier expressions
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "SIMPLE_VALUE"])
    builder.add_rule("QUALIFIED_VALUE", ["COLL_QUALIFIER", "QUALIFIED_VALUE"])
    
    return builder

def add_conjunction_grammar(
    builder: GrammarBuilder,
    conjunctions: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for conjunction expressions.
    
    Args:
        builder: The grammar builder to add rules to
        conjunctions: Optional list of conjunction terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    conjunctions = conjunctions or CONJUNCTIONS
    
    # Add conjunction terms
    builder.add_values("CONJUNCTION", conjunctions)
    
    # Add conjunction rules
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["SIMPLE_VALUE", "CONJUNCTION", "QUALIFIED_VALUE"])
    builder.add_rule("CONJUNCTION_VALUE", ["QUALIFIED_VALUE", "CONJUNCTION", "SIMPLE_VALUE"])
    
    # Register conjunction value as a value type
    builder.add_rule("VALUE", ["CONJUNCTION_VALUE"])
    
    return builder

def add_qualified_conjunction_grammar(builder: GrammarBuilder) -> GrammarBuilder:
    """
    Add grammar rules for qualified conjunctions.
    
    Args:
        builder: The grammar builder to add rules to
        
    Returns:
        The updated grammar builder
    """
    # Add qualified conjunction rules
    builder.add_rule("QUALIFIED_CONJUNCTION", ["COLL_QUALIFIER", "CONJUNCTION_VALUE"])
    
    # Register qualified conjunction as a value type
    builder.add_rule("VALUE", ["QUALIFIED_CONJUNCTION"])
    
    # Unit application to conjunctions (e.g., "5 or 10 mm")
    builder.add_rule("UNIT_VALUE", ["CONJUNCTION_VALUE", "UNIT"])
    
    return builder

def add_value_grammar(
    builder: GrammarBuilder,
    growth_forms: Optional[List[str]] = None,
    surface_terms: Optional[List[str]] = None,
    adjacent_qualifiers: Optional[List[str]] = None,
    collective_qualifiers: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    conjunctions: Optional[List[str]] = None,
    max_number: int = 100
) -> GrammarBuilder:
    """
    Add all grammar components for botanical value parsing.
    
    This function composes all the individual grammar components into a complete
    grammar for parsing botanical values.
    
    Args:
        builder: The grammar builder to add rules to
        growth_forms: Optional list of growth form terms
        surface_terms: Optional list of surface terms
        adjacent_qualifiers: Optional list of adjacent qualifiers
        collective_qualifiers: Optional list of collective qualifiers
        units: Optional list of measurement units
        conjunctions: Optional list of conjunctions
        max_number: Maximum number to include
        
    Returns:
        The updated grammar builder
    """
    # Add all grammar components
    builder = add_number_grammar(builder, max_number)
    builder = add_basic_terms_grammar(builder, growth_forms, surface_terms)
    builder = add_unit_grammar(builder, units)
    builder = add_adjacent_qualifier_grammar(builder, adjacent_qualifiers)
    builder = add_collective_qualifier_grammar(builder, collective_qualifiers)
    builder = add_conjunction_grammar(builder, conjunctions)
    builder = add_qualified_conjunction_grammar(builder)
    
    return builder

def build_jepson_grammar(
    growth_forms: Optional[List[str]] = None,
    surface_terms: Optional[List[str]] = None,
    adjacent_qualifiers: Optional[List[str]] = None,
    collective_qualifiers: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    conjunctions: Optional[List[str]] = None,
    max_number: int = 100,
    start_symbol: str = "VALUE"
) -> CFG:
    """
    Build a complete Jepson grammar for botanical value parsing.
    
    This is the main entry point for creating a grammar. It combines all the 
    modular grammar components with optional customizations.
    
    Args:
        growth_forms: Optional list of growth form terms
        surface_terms: Optional list of surface terms
        adjacent_qualifiers: Optional list of adjacent qualifiers
        collective_qualifiers: Optional list of collective qualifiers
        units: Optional list of measurement units
        conjunctions: Optional list of conjunctions
        max_number: Maximum number to include
        start_symbol: The start symbol for the grammar
        
    Returns:
        A context-free grammar for botanical values
    """
    builder = GrammarBuilder(start_symbol=start_symbol)
    
    builder = add_value_grammar(
        builder,
        growth_forms=growth_forms,
        surface_terms=surface_terms,
        adjacent_qualifiers=adjacent_qualifiers,
        collective_qualifiers=collective_qualifiers,
        units=units,
        conjunctions=conjunctions,
        max_number=max_number
    )
    
    return builder.build()
