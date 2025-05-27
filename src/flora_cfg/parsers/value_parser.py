"""
Value parser for botanical expressions.
"""
from typing import List
from nltk.parse import RecursiveDescentParser
from nltk.tokenize import word_tokenize

from src.flora_cfg.grammar.values import build_value_grammar
from src.flora_cfg.models.expression import (
    BotanicalExpression, 
    ValueExpression, 
    QualifierExpression, 
    ConjunctionExpression,
    RangeExpression
)

class BotanicalValueParser:
    """Parser for botanical value expressions using context-free grammar."""
    
    def __init__(self, custom_grammar=None):
        """
        Initialize the parser.
        
        Args:
            custom_grammar: Optional custom grammar to use
        """
        self.grammar = custom_grammar or build_value_grammar()
        self.parser = RecursiveDescentParser(self.grammar)
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the botanical text.
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of tokens
        """
        # Preprocess text to handle special tokens
        text = text.lower()
        text = text.replace("--", " -- ")
        
        # Use NLTK's word_tokenize
        tokens = word_tokenize(text)
        
        # Post-process to handle special cases
        processed_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Handle compound tokens like "to" after "--"
            if token == "--" and i + 1 < len(tokens) and tokens[i + 1] == "to":
                processed_tokens.append("--")
                i += 2
            else:
                processed_tokens.append(token)
                i += 1
        
        return processed_tokens
    
    def parse(self, text: str) -> BotanicalExpression:
        """
        Parse botanical text into an expression tree.
        
        Args:
            text: The text to parse
            
        Returns:
            A BotanicalExpression object
            
        Raises:
            ValueError: If the text cannot be parsed
        """
        # Tokenize the text
        tokens = self.tokenize(text)
        
        # Try to parse using the CFG
        trees = list(self.parser.parse(tokens))
        
        if not trees:
            # If the CFG parsing fails, fall back to a simple value
            if is_number(text):
                return ValueExpression(float(text), value_type="number")
            else:
                return ValueExpression(text, value_type="word")
        
        # Convert the parse tree to a BotanicalExpression
        return self._convert_tree_to_expression(trees[0])
    
    def _convert_tree_to_expression(self, tree) -> BotanicalExpression:
        """
        Convert an NLTK parse tree to a BotanicalExpression.
        
        Args:
            tree: The NLTK parse tree
            
        Returns:
            A BotanicalExpression object
        """
        # Extract the production for this node
        node_label = tree.label()
        
        # Handle leaf nodes
        if len(tree) == 1 and isinstance(tree[0], str):
            # This is a terminal node
            value = tree[0]
            
            # Check if it's a number
            if is_number(value):
                return ValueExpression(float(value), value_type="number")
            
            # Otherwise, it's a word
            return ValueExpression(value, value_type="word")
        
        # Handle qualified values
        if node_label == "QUALIFIED_VALUE":
            if len(tree) == 2:
                qualifier = tree[0][0]
                qualifier_type = "adjacent"
                
                # Determine qualifier type
                if tree[0].label() == "COLL_QUALIFIER":
                    qualifier_type = "collective"
                elif tree[0].label() == "ADJ_QUALIFIER":
                    qualifier_type = "adjacent"
                
                expression = self._convert_tree_to_expression(tree[1])
                return QualifierExpression(qualifier, expression, qualifier_type)
        
        # Handle unit values
        if node_label == "UNIT_VALUE":
            if len(tree) == 2:
                value = self._convert_tree_to_expression(tree[0])
                unit = tree[1][0]
                # Attach unit as qualifier
                return QualifierExpression(unit, value, qualifier_type="unit")
        
        # Handle conjunction expressions
        if node_label == "CONJUNCTION_VALUE":
            if len(tree) == 3:
                left = self._convert_tree_to_expression(tree[0])
                conj = tree[1][0]
                right = self._convert_tree_to_expression(tree[2])
                
                # Handle range expressions (like "1--5")
                if conj == "--" or conj == "to":
                    # Check if we have two numbers
                    if (isinstance(left, ValueExpression) and left.value_type == "number" and
                        isinstance(right, ValueExpression) and right.value_type == "number"):
                        # This is a range
                        return RangeExpression(left, right)
                
                return ConjunctionExpression(conj, [left, right])
        
        # Handle simple values
        if node_label == "SIMPLE_VALUE" or node_label == "VALUE":
            if len(tree) == 1:
                return self._convert_tree_to_expression(tree[0])
        
        # Recursively process non-terminal nodes
        for child in tree:
            if not isinstance(child, str):
                return self._convert_tree_to_expression(child)
        
        # Fallback: return a simple value
        return ValueExpression(str(tree), value_type="word")

def is_number(s: str) -> bool:
    """
    Check if a string can be converted to a number.
    
    Args:
        s: The string to check
        
    Returns:
        True if the string is a number, False otherwise
    """
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False
