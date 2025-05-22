# Jepson Parser

The Jepson Parser is a Python tool for extracting structured botanical data from Jepson eFlora-style plant descriptions. It uses a schema-driven approach to parse natural language into a hierarchical feature tree, enabling downstream analysis and data integration.

## Overview
- **Input:** Free-text Jepson taxon descriptions (e.g., "Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many...")
- **Output:** A tree of features (as `FeatureNode` objects), capturing plant traits and measurements in a structured format.
- **How it works:**
  - Uses configurable schemas and regular expressions to identify and extract features for plant habit, stem, leaf, and more.
  - Organizes extracted data in a hierarchical tree for easy traversal and export.

## Example Usage
```python
from src.feature_schema import get_jepson_feature_schema

description = '''
Habit: shrub or thicket-forming, 8--25 dm. Stem: prickles few to many, paired or not, 3--15 mm, thick-based and compressed, generally curved (straight). Leaf: axis +- shaggy-hairy (+- glabrous), hairs to 1 mm, glandless or glandular; leaflets 5--7(9), +- hairy, sometimes glandular; terminal leaflet generally 15--50 mm, +- ovate-elliptic, generally widest at or below middle, tip rounded to acute, margins single- or double-toothed, glandular or not. Inflorescence: (1)3--30(50)-flowered; ...'''

schema = get_jepson_feature_schema()
tree = schema.extract(description)
print(tree)
# tree.to_dict() for a JSON-serializable structure
```

## Project Structure
```
project/
├── src/
│   ├── jepson_parser.py      # Main parser interface
│   ├── feature_extractor.py  # Core extraction logic
│   ├── feature_node.py       # Feature tree node class
│   ├── feature_schema.py     # Schema definitions
│   └── feature_value.py      # Value/range handling
├── tests/                    # Test files
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests
```bash
pytest
```

## Notes
- The parser is schema-driven and can be extended for new features or other flora formats.
- See `src/jepson_parser.py` for more usage examples.
