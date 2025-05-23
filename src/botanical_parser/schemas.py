"""
Schema definitions for botanical descriptions.
"""
from .structure_extractor import StructureExtractor
from .attribute_extractor import AttributeExtractor
from .regex_utils import generate_attribute_regex, generate_numeric_regex


glandularity_extractor = AttributeExtractor("Glandularity", generate_attribute_regex(
    value_words=["glandless", "glandular", "eglandular"],
))

shape_extractor = AttributeExtractor("Shape", generate_attribute_regex(
    qualifiers=["generally", "mostly", "usually"],
    value_words=["ovoid", "obovoid", "globose", "pyriform", "ellipsoid", "cylindrical"],
))

erectness_extractor = AttributeExtractor("Erectness", generate_attribute_regex(
    qualifiers=["generally", "mostly", "usually"],
    value_words=["erect", "spreading", "reflexed", "appressed", "ascending"],
))

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
            AttributeExtractor("Height", generate_numeric_regex(
                units=["m", "cm", "dm", "mm", "ft"]
            )),
            
            AttributeExtractor("Growth Form", generate_attribute_regex(
                value_words=["shrub", "thicket-forming", "tree", "herb", "annual", "perennial", "vine", "subshrub"],
            )),

            erectness_extractor,
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
                    AttributeExtractor("Count", generate_attribute_regex(
                        value_words=["few", "many", "numerous", "sparse", "dense"],
                    )),
                    
                    AttributeExtractor("Grouping", generate_attribute_regex(
                        value_words=["paired", "clustered", "solitary", "scattered"],
                    )),
                    
                    AttributeExtractor("Length", generate_numeric_regex(
                        units=["mm", "cm"]
                    )),
                    
                    AttributeExtractor("Shape", generate_attribute_regex(
                        value_words=["thick-based", "compressed", "flattened", "conical", "cylindrical"],
                    )),
                    
                    AttributeExtractor("Curvature", generate_attribute_regex(
                        value_words=["curved", "straight", "recurved", "bent"]
                    )),
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
                    AttributeExtractor("Trichome Form", generate_attribute_regex(
                        qualifiers=["densely", "sparsely", "moderately", "\\+-"],
                        value_words=["shaggy-hairy", "hairy", "glabrous", "pubescent", "tomentose", "hirsute", "strigose", "villous"],
                    )),
                    
                    StructureExtractor(
                        name="Hair",
                        pattern=r"hairs\s+([^,;]+)",
                        attribute_extractors=[
                            AttributeExtractor("Length", r"to\s+([^,;]+)")
                        ]
                    ),

                    glandularity_extractor,
                ]
            ),
            StructureExtractor(
                name="Leaflet",
                pattern=r"leaflets\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Count", generate_numeric_regex(
                        units=[], # No units for count
                        allow_parenthetical=True
                    )),
                    
                    AttributeExtractor("Surface", generate_attribute_regex(
                        qualifiers=["densely", "sparsely", "\\+-"],
                        value_words=["hairy", "glabrous", "glandular", "pubescent", "tomentose", "hirsute"],
                    )),
                ]
            ),
            StructureExtractor(
                name="Terminal Leaflet",
                pattern=r"terminal\s+leaflet\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Size", generate_numeric_regex(
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        units=["mm", "cm"]
                    )),
                    
                    shape_extractor,
                    
                    AttributeExtractor("Width Position", r"widest\s+at\s+or\s+(below|above)\s+middle"),
                    
                    StructureExtractor(
                        name="Tip",
                        pattern=r"tip\s+(.+?)(?=;|$)",
                        attribute_extractors=[
                            shape_extractor,
                        ]
                    ),

                    StructureExtractor(
                        name="Margin",
                        pattern=r"margin\s+(.+?)(?=;|$)",
                        attribute_extractors=[
                            AttributeExtractor("Teeth", generate_attribute_regex(
                                value_words=["entire", "toothed", "serrate", "crenate", "dentate", "lobed", "single-toothed", "double-toothed"],
                            )),
                        ]
                    ),
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
                    AttributeExtractor("Width", generate_numeric_regex(
                        allow_decimal=True,
                        units=["mm", "cm"]
                    ) + r"\s+wide"),
                    
                    AttributeExtractor("Surface", generate_attribute_regex(
                        qualifiers=["densely", "sparsely", "moderately"],
                        value_words=["hairy", "glabrous", "pubescent", "tomentose"],
                    )),
                    
                    glandularity_extractor,
                ]
            ),
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    glandularity_extractor,
                    
                    AttributeExtractor("Margin", f"({generate_attribute_regex(
                        value_words=["entire", "toothed", "serrate", "ciliate"],                        
                    )})"),
                ]
            ),
            StructureExtractor(
                name="Petal",
                pattern=r"petals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    # Size pattern with qualifier and numeric range
                    AttributeExtractor("Size", generate_numeric_regex(
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        units=["mm", "cm"]
                    )),
                    
                    # Color pattern
                    AttributeExtractor("Color", f"({generate_attribute_regex(
                        qualifiers=["generally", "mostly", "usually", "pale", "bright", "dark"],
                        value_words=["pink", "white", "yellow", "purple", "red", "blue", "green", "orange", "lavender", "cream"],                        
                    )})"),
                ]
            ),
            StructureExtractor(
                name="Pistil",
                pattern=r"pistils\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Count", generate_numeric_regex(
                        units=[], # No units for count
                        allow_parenthetical=True
                    )),
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
            AttributeExtractor("Width", generate_numeric_regex(
                prefix_qualifiers=["generally", "mostly", "usually"],
                units=["mm", "cm"],
                allow_parenthetical=True
            ) + r"\s+wide"),
            
            shape_extractor,
        ],
        child_extractors=[
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    erectness_extractor,
                    
                    AttributeExtractor("Persistence", generate_attribute_regex(
                        value_words=["persistent", "deciduous", "caducous"],                        
                    )),
                ]
            ),
            StructureExtractor(
                name="Achene",
                pattern=r"achenes\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    AttributeExtractor("Size", generate_numeric_regex(
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        allow_decimal=True,
                        units=["mm", "cm"]
                    )),
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
