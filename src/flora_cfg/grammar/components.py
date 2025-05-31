"""
Modular grammar components for botanical value parsing.
"""
from typing import List, Optional, Dict
from nltk.grammar import Nonterminal
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

def add_number_grammar(
    builder: GrammarBuilder, 
    number: Nonterminal,
    simple_value: Nonterminal,
    value: Nonterminal,
    max_number: int = 100
) -> GrammarBuilder:
    """
    Add grammar rules for numeric values.
    
    Args:
        builder: The grammar builder to add rules to
        number: Nonterminal for number symbols
        simple_value: Nonterminal for simple values
        value: Nonterminal for values
        max_number: The maximum number to include
        
    Returns:
        The updated grammar builder
    """
    # Add number terminals
    for i in range(1, max_number + 1):
        builder.add_terminal_rule(number, str(i))
    
    # Register numbers as simple values
    builder.add_rule(simple_value, [number])
    
    # Make them valid values
    builder.add_rule(value, [simple_value])
    
    return builder

def add_basic_terms_grammar(
    builder: GrammarBuilder,
    growth_form: Nonterminal,
    surface: Nonterminal,
    simple_value: Nonterminal,
    value: Nonterminal,
    growth_forms: Optional[List[str]] = None,
    surface_terms: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for basic botanical terms.
    
    Args:
        builder: The grammar builder to add rules to
        growth_form: Nonterminal for growth form terms
        surface: Nonterminal for surface terms
        simple_value: Nonterminal for simple values
        value: Nonterminal for values
        growth_forms: Optional list of growth form terms (e.g., "herb", "shrub")
        surface_terms: Optional list of surface terms (e.g., "glabrous", "hairy")
        
    Returns:
        The updated grammar builder
    """
    # Use provided lists or defaults
    growth_forms = growth_forms or GROWTH_FORMS
    surface_terms = surface_terms or SURFACE_TERMS
    
    # Add basic terms
    builder.add_values(growth_form, growth_forms)
    builder.add_values(surface, surface_terms)
    
    # Register as simple values
    builder.add_rule(simple_value, [growth_form])
    builder.add_rule(simple_value, [surface])
    
    # Make them valid values
    builder.add_rule(value, [simple_value])
    
    return builder

def add_unit_grammar(
    builder: GrammarBuilder,
    # Required nonterminals (dependencies)
    number: Nonterminal,
    value: Nonterminal,
    adj_qualifier: Nonterminal,
    # Nonterminals this function creates/uses
    unit: Nonterminal,
    unit_value: Nonterminal,
    qualified_number: Nonterminal,
    # Optional parameters
    units: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for units of measurement.
    
    Args:
        builder: The grammar builder to add rules to
        number: Nonterminal for number symbols (dependency)
        value: Nonterminal for values (dependency)
        adj_qualifier: Nonterminal for adjacent qualifiers (dependency)
        unit: Nonterminal for unit symbols
        unit_value: Nonterminal for values with units
        qualified_number: Nonterminal for qualified numbers
        units: Optional list of unit terms (e.g., "mm", "cm")
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    units = units or UNITS
    
    # Add unit terms
    builder.add_values(unit, units)
    
    # Add unit expressions
    builder.add_rule(unit_value, [number, unit])
    builder.add_rule(unit_value, [qualified_number, unit])
    builder.add_rule(qualified_number, [adj_qualifier, number])
    
    # Make them valid values
    builder.add_rule(value, [unit_value])
    
    return builder

def add_adjacent_qualifier_grammar(
    builder: GrammarBuilder,
    # Required nonterminals (dependencies)
    simple_value: Nonterminal,
    value: Nonterminal,
    # Nonterminals this function creates/uses
    adj_qualifier: Nonterminal,
    qualified_value: Nonterminal,
    # Optional parameters
    qualifiers: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for adjacent qualifiers.
    
    Args:
        builder: The grammar builder to add rules to
        simple_value: Nonterminal for simple values (dependency)
        value: Nonterminal for values (dependency)
        adj_qualifier: Nonterminal for adjacent qualifiers
        qualified_value: Nonterminal for qualified values
        qualifiers: Optional list of adjacent qualifier terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    qualifiers = qualifiers or ADJACENT_QUALIFIERS
    
    # Add qualifier terms
    builder.add_values(adj_qualifier, qualifiers)
    
    # Add qualifier expressions
    builder.add_rule(qualified_value, [adj_qualifier, simple_value])
    
    # Make them valid values
    builder.add_rule(value, [qualified_value])
    
    return builder

def add_collective_qualifier_grammar(
    builder: GrammarBuilder,
    # Required nonterminals (dependencies)
    value: Nonterminal,
    # Nonterminals this function creates/uses
    coll_qualifier: Nonterminal,
    qualified_value: Nonterminal,
    # Optional parameters
    qualifiers: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for collective qualifiers.
    
    Args:
        builder: The grammar builder to add rules to
        value: Nonterminal for values (dependency)
        coll_qualifier: Nonterminal for collective qualifiers
        qualified_value: Nonterminal for qualified values
        qualifiers: Optional list of collective qualifier terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    qualifiers = qualifiers or COLLECTIVE_QUALIFIERS
    
    # Add qualifier terms
    builder.add_values(coll_qualifier, qualifiers)
    
    # Add qualifier expressions - single level only, no recursion
    builder.add_rule(qualified_value, [coll_qualifier, value])
    
    # Note: We intentionally do not add a recursive rule like:
    # builder.add_rule(qualified_value, [coll_qualifier, qualified_value])
    # This would cause infinite recursion during parsing.
    # Instead, we only allow a single collective qualifier per value.
    # Multiple qualifiers can still be handled by the parser through multiple parsing passes.
    
    return builder

def add_conjunction_grammar(
    builder: GrammarBuilder,
    # Required nonterminals (dependencies)
    simple_value: Nonterminal,
    value: Nonterminal,
    qualified_value: Nonterminal,
    # Nonterminals this function creates/uses
    conjunction: Nonterminal,
    conjunction_value: Nonterminal,
    # Optional parameters
    conjunctions: Optional[List[str]] = None
) -> GrammarBuilder:
    """
    Add grammar rules for conjunction expressions.
    
    Args:
        builder: The grammar builder to add rules to
        simple_value: Nonterminal for simple values (dependency)
        value: Nonterminal for values (dependency)
        qualified_value: Nonterminal for qualified values (dependency)
        conjunction: Nonterminal for conjunction symbols
        conjunction_value: Nonterminal for conjunction expressions
        conjunctions: Optional list of conjunction terms
        
    Returns:
        The updated grammar builder
    """
    # Use provided list or default
    conjunctions = conjunctions or CONJUNCTIONS
    
    # Add conjunction terms
    builder.add_values(conjunction, conjunctions)
    
    # Add conjunction expressions (MODIFIED to avoid recursion)
    builder.add_rule(conjunction_value, [simple_value, conjunction, simple_value])
    
    # The following rules were removed to prevent infinite recursion:
    # builder.add_rule(conjunction_value, [simple_value, conjunction, value])
    # builder.add_rule(conjunction_value, [value, conjunction, simple_value])
    
    # Allow qualified values to be combined with simple values in conjunctions
    builder.add_rule(conjunction_value, [qualified_value, conjunction, simple_value])
    builder.add_rule(conjunction_value, [simple_value, conjunction, qualified_value])
    
    # Add specific rule for qualified-qualified conjunctions without introducing recursion
    builder.add_rule(conjunction_value, [qualified_value, conjunction, qualified_value])
    
    # Register conjunction value as a value type
    builder.add_rule(value, [conjunction_value])
    
    return builder

def add_qualified_conjunction_grammar(
    builder: GrammarBuilder,
    # Required nonterminals (dependencies)
    value: Nonterminal,
    coll_qualifier: Nonterminal,
    conjunction_value: Nonterminal,
    unit: Nonterminal,
    unit_value: Nonterminal,
    # Nonterminals this function creates
    qualified_conjunction: Nonterminal
) -> GrammarBuilder:
    """
    Add grammar rules for qualified conjunctions.
    
    Args:
        builder: The grammar builder to add rules to
        value: Nonterminal for values (dependency)
        coll_qualifier: Nonterminal for collective qualifiers (dependency)
        conjunction_value: Nonterminal for conjunction expressions (dependency)
        unit: Nonterminal for unit symbols (dependency)
        unit_value: Nonterminal for unit values (dependency)
        qualified_conjunction: Nonterminal for qualified conjunctions
        
    Returns:
        The updated grammar builder
    """
    # Add qualified conjunction rules
    builder.add_rule(qualified_conjunction, [coll_qualifier, conjunction_value])
    
    # Register qualified conjunction as a value type
    builder.add_rule(value, [qualified_conjunction])
    
    # Unit application to conjunctions (e.g., "5 or 10 mm")
    builder.add_rule(unit_value, [conjunction_value, unit])
    
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
    # Create all the nonterminals we need
    number = Nonterminal("NUMBER")
    simple_value = Nonterminal("SIMPLE_VALUE")
    value = Nonterminal("VALUE")
    growth_form = Nonterminal("GROWTH_FORM")
    surface = Nonterminal("SURFACE")
    unit = Nonterminal("UNIT")
    unit_value = Nonterminal("UNIT_VALUE")
    qualified_number = Nonterminal("QUALIFIED_NUMBER")
    adj_qualifier = Nonterminal("ADJ_QUALIFIER")
    qualified_value = Nonterminal("QUALIFIED_VALUE")
    coll_qualifier = Nonterminal("COLL_QUALIFIER")
    conjunction = Nonterminal("CONJUNCTION")
    conjunction_value = Nonterminal("CONJUNCTION_VALUE")
    qualified_conjunction = Nonterminal("QUALIFIED_CONJUNCTION")
    
    # Add all grammar components with explicit nonterminals
    builder = add_number_grammar(
        builder, number, simple_value, value, max_number
    )
    
    builder = add_basic_terms_grammar(
        builder, growth_form, surface, simple_value, value, 
        growth_forms, surface_terms
    )
    
    builder = add_unit_grammar(
        builder, number, value, adj_qualifier, unit, unit_value, 
        qualified_number, units
    )
    
    builder = add_adjacent_qualifier_grammar(
        builder, simple_value, value, adj_qualifier, qualified_value, 
        adjacent_qualifiers
    )
    
    builder = add_collective_qualifier_grammar(
        builder, value, coll_qualifier, qualified_value, 
        collective_qualifiers
    )
    
    builder = add_conjunction_grammar(
        builder, simple_value, value, qualified_value, 
        conjunction, conjunction_value, conjunctions
    )
    
    builder = add_qualified_conjunction_grammar(
        builder, value, coll_qualifier, conjunction_value, 
        unit, unit_value, qualified_conjunction
    )
    
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
    # Create the start symbol nonterminal
    start_nt = Nonterminal(start_symbol)
    
    # Initialize the builder with the start symbol
    builder = GrammarBuilder(start_symbol=start_nt)
    
    # Add all grammar components
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
