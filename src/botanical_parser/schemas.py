"""
Schema definitions for botanical descriptions.
"""
from .structure_extractor import StructureExtractor
from .attribute_extractor import AttributeExtractor


def get_habit_schema() -> StructureExtractor:
    """
    Create a schema for extracting habit information.
    
    Returns:
        A structure extractor for habit.
    """
    return StructureExtractor(
        name="Habit",
        pattern=r"Habit:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[
            AttributeExtractor("Height", r"(\d+--\d+\s*[a-z]+)"),
            AttributeExtractor("Growth Form", r"((?:shrub|thicket-forming|tree|herb|annual|perennial)(?:\s+or\s+(?:shrub|thicket-forming|tree|herb|annual|perennial))*)"),
        ]
    )


def get_stem_schema() -> StructureExtractor:
    """
    Create a schema for extracting stem information.
    
    Returns:
        A structure extractor for stem.
    """
    return StructureExtractor(
        name="Stem",
        pattern=r"Stem:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[],
        child_extractors=[
            StructureExtractor(
                name="Prickle",
                pattern=r"prickles\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Count", r"(few[- ]to[- ]many|few|many)"),
                    AttributeExtractor("Grouping", r"(paired[- ]or[- ]not|paired)"),
                    AttributeExtractor("Length", r"(\d+--\d+\s*mm)"),
                    AttributeExtractor("Shape", r"(thick-based[- ]and[- ]compressed|thick-based|compressed)"),
                    AttributeExtractor("Curvature", r"(generally[- ]curved[- ]\(straight\)|curved|straight)"),
                ]
            )
        ]
    )


def get_leaf_schema() -> StructureExtractor:
    """
    Create a schema for extracting leaf information.
    
    Returns:
        A structure extractor for leaf.
    """
    return StructureExtractor(
        name="Leaf",
        pattern=r"Leaf:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[],
        child_extractors=[
            StructureExtractor(
                name="Axis",
                pattern=r"axis\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Trichome Form", r"(shaggy-hairy|glabrous)"),
                    AttributeExtractor("Hair Length", r"hairs\s+to\s+([^,;]+)"),
                    AttributeExtractor("Glandularity", r"(glandless|glandular)"),
                ]
            ),
            StructureExtractor(
                name="Leaflet",
                pattern=r"leaflets\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Count", r"(\d+--\d+(?:\(\d+\))?)"),
                    AttributeExtractor("Surface", r"(hairy|glabrous|glandular)"),
                ]
            ),
            StructureExtractor(
                name="Terminal Leaflet",
                pattern=r"terminal\s+leaflet\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Size", r"generally\s+(\d+--\d+\s*mm)"),
                    AttributeExtractor("Shape", r"(ovate-elliptic)"),
                    AttributeExtractor("Width Position", r"widest\s+at\s+or\s+(below|above)\s+middle"),
                    AttributeExtractor("Tip", r"tip\s+(rounded|acute)"),
                    AttributeExtractor("Margin", r"margins\s+(single-\s*or\s*double-toothed)"),
                ]
            )
        ]
    )


def get_flower_schema() -> StructureExtractor:
    """
    Create a schema for extracting flower information.
    
    Returns:
        A structure extractor for flower.
    """
    return StructureExtractor(
        name="Flower",
        pattern=r"Flower:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[],
        child_extractors=[
            StructureExtractor(
                name="Hypanthium",
                pattern=r"hypanthium\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Width", r"(\d+(?:\.\d+)?--\d+(?:\.\d+)?\s*mm)\s+wide"),
                    AttributeExtractor("Surface", r"(glabrous|hairy|sparsely\s+hairy)"),
                    AttributeExtractor("Glandularity", r"(glandless|glandular)"),
                ]
            ),
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Glandularity", r"(glandular\s+or\s+not|glandless|glandular)"),
                    AttributeExtractor("Margin", r"(entire)"),
                ]
            ),
            StructureExtractor(
                name="Petal",
                pattern=r"petals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Size", r"generally\s+(\d+--\d+\s*mm)"),
                    AttributeExtractor("Color", r"(pink|white|yellow|purple|red)"),
                ]
            ),
            StructureExtractor(
                name="Pistil",
                pattern=r"pistils\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Count", r"(\d+--\d+)"),
                ]
            )
        ]
    )


def get_fruit_schema() -> StructureExtractor:
    """
    Create a schema for extracting fruit information.
    
    Returns:
        A structure extractor for fruit.
    """
    return StructureExtractor(
        name="Fruit",
        pattern=r"Fruit:\s*(.+?)(?=\n\w+:|$)",
        attribute_extractors=[
            AttributeExtractor("Width", r"generally\s+(\d+--\d+(?:\(\d+\))?\s*mm)\s+wide"),
            AttributeExtractor("Shape", r"generally\s+\((ob)ovoid\)"),
        ],
        child_extractors=[
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Position", r"generally\s+(erect)"),
                    AttributeExtractor("Persistence", r"(persistent)"),
                ]
            ),
            StructureExtractor(
                name="Achene",
                pattern=r"achenes\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Size", r"generally\s+(\d+(?:\.\d+)?--\d+(?:\.\d+)?\s*mm)"),
                ]
            )
        ]
    )


def get_jepson_schema() -> StructureExtractor:
    """
    Create the root schema for a Jepson-style botanical description.
    
    Returns:
        A root structure extractor for Jepson descriptions.
    """
    return StructureExtractor(
        name="TaxonDescription",
        pattern=None,  # Root level has no pattern
        child_extractors=[
            get_habit_schema(),
            get_stem_schema(),
            get_leaf_schema(),
            get_flower_schema(),
            get_fruit_schema()
        ]
    )
