"""
Utility functions for generating regex patterns for botanical descriptions.
"""
from typing import List, Optional


def generate_attribute_regex(
    value_words: List[str],
    qualifiers: Optional[List[str]] = None,
    conjunctions: Optional[List[str]] = None
) -> str:
    """
    Generate a regex pattern for matching botanical attribute descriptions.
    
    Args:
        value_words: List of specific value words to match (e.g., "curved", "hairy")
        qualifiers: Optional list of qualifier words/symbols (e.g., "generally", "+-", "sparsely")
        conjunctions: Optional list of conjunction words (e.g., "or", "and", "to")
        
    Returns:
        A regex pattern string
    
    Examples of matched patterns:
        - "shrub or thicket-forming"
        - "few to many"
        - "thick-based and compressed"
        - "generally curved"
        - "+- shaggy-hairy"
        - "glandless or glandular"
        - "glabrous to sparsely hairy"
        - "generally erect"
    """
    # Default lists if none provided
    qualifiers = qualifiers or [
        "generally", "mostly", "sometimes", "rarely", "often", 
        "usually", "primarily", "mainly", "sparsely", "densely", 
        "highly", "slightly", "moderately", "\\+-", "few", "many",
        "several", "numerous", "occasional", "frequent", "abundant",
        "sparse", "dense", "thick"
    ]
    
    conjunctions = conjunctions or [
        "and", "or", "to", "through", "with", "without"
    ]
    
    # Build the qualifier pattern - optional qualifier at start or after conjunction
    qualifier_pattern = r"(?:{})?".format("|".join(qualifiers)) if qualifiers else ""
    
    # Build the conjunction pattern - optional conjunction between value words
    conjunction_pattern = r"(?:\s+(?:{})\s+)?".format("|".join(conjunctions)) if conjunctions else ""
    
    # Build the value word pattern
    value_word_pattern = r"(?:{})".format("|".join(value_words))
    
    # Build the complete pattern
    # This handles expressions like:
    # - "qualifier value-word"
    # - "value-word conjunction value-word"
    # - "qualifier value-word conjunction qualifier value-word"
    
    # Start with optional qualifier followed by a value word
    pattern = r"(?:{}(?:\s+))?{}".format(qualifier_pattern, value_word_pattern)
    
    # Add ability to have repeating conjunction + optional qualifier + value word combinations
    pattern += r"(?:{}(?:{}(?:\s+))?{})*(\.)?".format(
        conjunction_pattern, qualifier_pattern, value_word_pattern
    )
    
    # TODO: Capture group is expected by AttributeExtractor, should we decouple matching and extracting?
    return r"({})".format(pattern)


def generate_numeric_regex(
    prefix_qualifiers: Optional[List[str]] = None,
    allow_decimal: bool = True,
    allow_parenthetical: bool = True,
    units: Optional[List[str]] = None
) -> str:
    """
    Generate a regex pattern for matching numeric ranges in botanical descriptions.
    
    Args:
        prefix_qualifiers: Optional list of qualifier words that may precede the range
        allow_decimal: Whether to allow decimal numbers
        allow_parenthetical: Whether to allow parenthetical values like in "1--5(10) mm"
        units: Optional list of unit words that may follow the range
        
    Returns:
        A regex pattern string
    
    Examples of matched patterns:
        - "1--5 mm"
        - "generally 1--5 mm"
        - "1.5--3.2 cm"
        - "1--5(10) mm"
    """
    # Default lists if none provided
    prefix_qualifiers = prefix_qualifiers or [
        "generally", "mostly", "usually", "approximately", 
        "ca", "ca.", "about", "up to", "to"
    ]
    
    units = units or ["mm", "cm", "m", "dm"]
    
    # Build the qualifier pattern - optional qualifier at start
    qualifier_pattern = r"(?:{})\s+".format("|".join(prefix_qualifiers)) if prefix_qualifiers else ""
    
    # Build the number pattern based on whether decimals are allowed
    if allow_decimal:
        number_pattern = r"(\d+(?:\.\d+)?)"
    else:
        number_pattern = r"(\d+)"
    
    # Build the parenthetical pattern if allowed
    parenthetical_pattern = r"(?:\((\d+(?:\.\d+)?)\))?" if allow_parenthetical else ""
    
    # Build the units pattern
    units_pattern = r"(?:\s*(?:{}))?" .format("|".join(units)) if units else ""
    
    # Complete pattern: optional qualifier + first number + -- + second number + optional parenthetical + optional units
    pattern = r"(?:{})?{}--{}{}{}".format(
        qualifier_pattern, 
        number_pattern, 
        number_pattern,
        parenthetical_pattern, 
        units_pattern
    )
    
    # TODO: Capture group is expected by AttributeExtractor, should we decouple matching and extracting?
    return r"({})".format(pattern)