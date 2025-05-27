"""
Core grammar building components for the Flora CFG parser.
"""
from typing import List, Union
from nltk.grammar import Nonterminal, Production, CFG

class GrammarBuilder:
    """
    Builder class for constructing context-free grammars programmatically.
    Provides a fluent interface for defining grammar rules.
    """
    
    def __init__(self, start_symbol: str = "S"):
        """
        Initialize a grammar builder with a start symbol.
        
        Args:
            start_symbol: The starting non-terminal symbol of the grammar
        """
        self.productions = []
        self.nonterminals = {}
        self.start_symbol = self._get_nonterminal(start_symbol)
        
    def _get_nonterminal(self, name: str) -> Nonterminal:
        """
        Get or create a non-terminal with the given name.
        
        Args:
            name: The name of the non-terminal
            
        Returns:
            A Nonterminal object
        """
        if name not in self.nonterminals:
            self.nonterminals[name] = Nonterminal(name)
        return self.nonterminals[name]
    
    def add_rule(self, lhs: str, rhs: List[Union[str, Nonterminal]]) -> 'GrammarBuilder':
        """
        Add a production rule to the grammar.
        
        Args:
            lhs: The left-hand side non-terminal
            rhs: The right-hand side sequence of terminals and non-terminals
            
        Returns:
            Self for method chaining
        """
        lhs_nt = self._get_nonterminal(lhs)
        rhs_items = []
        
        for item in rhs:
            if isinstance(item, str) and item.isupper() and not item.startswith('"') and not item.endswith('"'):
                # Treat uppercase strings as non-terminals unless quoted
                rhs_items.append(self._get_nonterminal(item))
            else:
                # Treat other items as terminals
                rhs_items.append(item)
        
        self.productions.append(Production(lhs_nt, rhs_items))
        return self
    
    def add_terminal_rule(self, lhs: str, terminal: str) -> 'GrammarBuilder':
        """
        Add a rule that produces a terminal symbol.
        
        Args:
            lhs: The left-hand side non-terminal
            terminal: The terminal symbol
            
        Returns:
            Self for method chaining
        """
        return self.add_rule(lhs, [terminal])
    
    def add_alternative_rules(self, lhs: str, alternatives: List[List[Union[str, Nonterminal]]]) -> 'GrammarBuilder':
        """
        Add multiple alternative production rules for the same LHS.
        
        Args:
            lhs: The left-hand side non-terminal
            alternatives: List of alternative RHS expansions
            
        Returns:
            Self for method chaining
        """
        for alt in alternatives:
            self.add_rule(lhs, alt)
        return self
    
    def add_values(self, lhs: str, values: List[str]) -> 'GrammarBuilder':
        """
        Add rules for a list of terminal values.
        
        Args:
            lhs: The left-hand side non-terminal
            values: List of terminal values
            
        Returns:
            Self for method chaining
        """
        for value in values:
            self.add_terminal_rule(lhs, value)
        return self
    
    def build(self) -> CFG:
        """
        Build and return the context-free grammar.
        
        Returns:
            A CFG object
        """
        return CFG(self.start_symbol, self.productions)
