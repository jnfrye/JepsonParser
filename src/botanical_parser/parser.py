"""
Main parser interface for botanical descriptions.
"""
import logging
from .structure_node import StructureNode
from .structure_extractor import StructureExtractor
from .schemas import get_jepson_schema

# Configure logging
logger = logging.getLogger(__name__)


def parse_description(text: str, schema: StructureExtractor = None) -> StructureNode:
    """
    Parse a botanical description into a structured tree.
    
    Args:
        text: The botanical description text to parse.
        schema: Optional custom schema extractor to use.
                If not provided, the default Jepson schema will be used.
    
    Returns:
        Root structure node containing the parsed description.
    """
    if schema is None:
        schema = get_jepson_schema()
        
    logger.info(f"Parsing botanical description with schema {schema.name}")
    return schema.extract(text)
