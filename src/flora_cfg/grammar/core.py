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
    
    def __init__(self, start_symbol: Nonterminal):
        """
        Initialize a grammar builder with a start symbol.
        
        Args:
            start_symbol: The starting non-terminal symbol of the grammar
        """
        self.productions = []
        self.nonterminals = {start_symbol.symbol(): start_symbol}
        self.start_symbol = start_symbol
    
    def add_rule(self, lhs: Nonterminal, rhs: List[Union[str, Nonterminal]]) -> 'GrammarBuilder':
        """
        Add a production rule to the grammar.
        
        Args:
            lhs: The left-hand side non-terminal
            rhs: The right-hand side sequence of terminals and non-terminals
            
        Returns:
            Self for method chaining
        """
        # Register the nonterminal if it's not already known
        if lhs.symbol() not in self.nonterminals:
            self.nonterminals[lhs.symbol()] = lhs
            
        rhs_items = []
        
        for item in rhs:
            if isinstance(item, Nonterminal):
                # Register the nonterminal if it's not already known
                if item.symbol() not in self.nonterminals:
                    self.nonterminals[item.symbol()] = item
                rhs_items.append(item)
            else:
                # Treat other items as terminals
                rhs_items.append(item)
        
        self.productions.append(Production(lhs, rhs_items))
        return self
    
    def add_terminal_rule(self, lhs: Nonterminal, terminal: str) -> 'GrammarBuilder':
        """
        Add a rule that produces a terminal symbol.
        
        Args:
            lhs: The left-hand side non-terminal
            terminal: The terminal symbol
            
        Returns:
            Self for method chaining
        """
        return self.add_rule(lhs, [terminal])
    
    def add_alternative_rules(self, lhs: Nonterminal, alternatives: List[List[Union[str, Nonterminal]]]) -> 'GrammarBuilder':
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
    
    def add_values(self, lhs: Nonterminal, values: List[str]) -> 'GrammarBuilder':
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
    
    def merge(self, other_builder: 'GrammarBuilder') -> 'GrammarBuilder':
        """
        Merge another grammar builder into this one.
        
        Args:
            other_builder: Another GrammarBuilder to merge
            
        Returns:
            Self, for method chaining
        """
        # Merge productions
        self.productions.extend(other_builder.productions)
        
        # Merge nonterminals
        for name, nt in other_builder.nonterminals.items():
            if name not in self.nonterminals:
                self.nonterminals[name] = nt
        
        return self
    
    def build(self) -> CFG:
        """
        Build and return the context-free grammar.
        
        Returns:
            A CFG object
        """
        return CFG(self.start_symbol, self.productions)
