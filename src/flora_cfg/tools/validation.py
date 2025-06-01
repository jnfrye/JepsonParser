"""
Validation tools for testing the botanical parser against real descriptions.
"""
import json
import os
from typing import Dict, List

from src.flora_cfg.parsers.value_parser import BotanicalValueParser
from src.flora_cfg.models.expression import ValueExpression

def validate_botanical_phrases(description: str) -> Dict[str, List]:
    """
    Validate a botanical description against the parser.
    
    Args:
        description: Botanical description to test
        
    Returns:
        Dictionary with 'success' and 'failure' lists
    """
    parser = BotanicalValueParser()
    results = {
        "success": [],
        "failure": []
    }
    
    try:
        result = parser.parse(description)
        
        # Check if it was a true parse or fallback
        # If it's a simple ValueExpression with the exact input text, it was likely a fallback        
        if isinstance(result, ValueExpression) and result.value_type == "parse failure":
            raise ValueError(f"Parse failure; fell back to simple value: '{result.value}'")
            
        results["success"].append({
            "description": description,
            "parsed_as": str(result),
            "expression_type": result.__class__.__name__
        })
        
    except ValueError as e:
        results["failure"].append({
            "description": description,
            "error": str(e)
        })
    
    return results

def save_validation_results(results: Dict[str, List], filename: str) -> None:
    """
    Save validation results to a JSON file.
    
    Args:
        results: Dictionary with validation results
        filename: Path to save the JSON file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

def run_validation(description_file: str, output_file: str = 'validation_results.json') -> Dict:
    """
    Main function to run validation on a file of descriptions.
    
    Args:
        description_file: Path to file containing botanical descriptions
        output_file: Path to save validation results
        
    Returns:
        Dictionary with validation results
    """
    # Read descriptions from file
    with open(description_file, 'r') as f:
        description = f.read().strip()

    # Run validation
    results = validate_botanical_phrases(description)
    
    # Save results
    save_validation_results(results, output_file)
    
    # Return results for further processing if needed
    return results
