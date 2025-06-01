#!/usr/bin/env python
"""
Script to run the botanical parser against real descriptions.
"""
import argparse
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from src.flora_cfg.tools.validation import run_validation

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run botanical parser on real descriptions.')
    parser.add_argument('input_file', help='File containing botanical descriptions')
    parser.add_argument('--output', '-o', default='results/parse_results.json',
                       help='Output file for parse results (default: results/parse_results.json)')
    return parser.parse_args()

def main():
    """Main function to run the parser test."""
    args = parse_args()
    
    results = run_validation(args.input_file, args.output)
    
    # Print summary
    total_phrases = len(results['success']) + len(results['failure'])
    success_rate = len(results['success']) / total_phrases * 100 if total_phrases else 0
    
    print("\nParsing Summary:")
    print(f"Total phrases: {total_phrases}")
    print(f"Successfully parsed: {len(results['success'])} ({success_rate:.1f}%)")
    print(f"Failed to parse: {len(results['failure'])}")

if __name__ == "__main__":
    main()
