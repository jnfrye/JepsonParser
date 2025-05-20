# Python Project with Unit Testing

A simple Python project with unit testing setup using pytest.

## Project Structure
```
project/
├── src/              # Source code
│   └── calculator.py # Example module
├── tests/           # Test files
│   └── test_calculator.py
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests
```bash
pytest
```
