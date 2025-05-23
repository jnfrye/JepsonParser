"""
Schema definitions for botanical descriptions.
"""
from .structure_extractor import StructureExtractor
from .attribute_extractor import NumericAttributeExtractor, QualitativeAttributeExtractor


glandularity_extractor = QualitativeAttributeExtractor(
    name="Glandularity", 
    value_words=["glandless", "glandular", "eglandular"]
)

shape_extractor = QualitativeAttributeExtractor(
    name="Shape",
    qualifiers=["generally", "mostly", "usually"],
    value_words=["ovoid", "obovoid", "globose", "pyriform", "ellipsoid", "cylindrical"]
)

erectness_extractor = QualitativeAttributeExtractor(
    name="Erectness",
    qualifiers=["generally", "mostly", "usually"],
    value_words=["erect", "spreading", "reflexed", "appressed", "ascending"]
)

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
            NumericAttributeExtractor(
                name="Height",
                units=["m", "cm", "dm", "mm", "ft"]
            ),
            
            QualitativeAttributeExtractor(
                name="Growth Form",
                value_words=["shrub", "thicket-forming", "tree", "herb", "annual", "perennial", "vine", "subshrub"]
            ),

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
                    QualitativeAttributeExtractor(
                        name="Count",
                        value_words=["few", "many", "numerous", "sparse", "dense"]
                    ),
                    
                    QualitativeAttributeExtractor(
                        name="Grouping",
                        value_words=["paired", "clustered", "solitary", "scattered"]
                    ),
                    
                    NumericAttributeExtractor(
                        name="Length",
                        units=["mm", "cm"]
                    ),
                    
                    QualitativeAttributeExtractor(
                        name="Shape",
                        value_words=["thick-based", "compressed", "flattened", "conical", "cylindrical"]
                    ),
                    
                    QualitativeAttributeExtractor(
                        name="Curvature",
                        value_words=["curved", "straight", "recurved", "bent"]
                    ),
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
                    QualitativeAttributeExtractor(
                        name="Trichome Form",
                        qualifiers=["densely", "sparsely", "moderately", "\\+-"],
                        value_words=["shaggy-hairy", "hairy", "glabrous", "pubescent", "tomentose", "hirsute", "strigose", "villous"]
                    ),
                    
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
                    NumericAttributeExtractor(
                        name="Count",
                        units=[],  # No units for count
                    ),
                    
                    QualitativeAttributeExtractor(
                        name="Surface",
                        qualifiers=["densely", "sparsely", "\\+-"],
                        value_words=["hairy", "glabrous", "glandular", "pubescent", "tomentose", "hirsute"]
                    ),
                ]
            ),
            StructureExtractor(
                name="Terminal Leaflet",
                pattern=r"terminal\s+leaflet\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    NumericAttributeExtractor(
                        name="Size",
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        units=["mm", "cm"]
                    ),
                    
                    shape_extractor,
                    
                    QualitativeAttributeExtractor(
                        name="Width Position",
                        value_words=["below", "above"]
                    ),
                    
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
                    NumericAttributeExtractor(
                        name="Width",
                        allow_decimal=True,
                        units=["mm", "cm"]
                    ),
                    
                    QualitativeAttributeExtractor(
                        name="Pubescence",
                        qualifiers=["densely", "sparsely", "moderately"],
                        value_words=["hairy", "glabrous", "pubescent", "tomentose"]
                    ),
                    
                    glandularity_extractor,
                ]
            ),
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    glandularity_extractor,
                    
                    QualitativeAttributeExtractor(
                        name="Margin",
                        value_words=["entire", "toothed", "serrate", "ciliate"]
                    ),
                ]
            ),
            StructureExtractor(
                name="Petal",
                pattern=r"petals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    # Size pattern with qualifier and numeric range
                    NumericAttributeExtractor(
                        name="Size",
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        units=["mm", "cm"]
                    ),
                    
                    # Color pattern
                    QualitativeAttributeExtractor(
                        name="Color",
                        qualifiers=["generally", "mostly", "usually", "pale", "bright", "dark"],
                        value_words=["pink", "white", "yellow", "purple", "red", "blue", "green", "orange", "lavender", "cream"]
                    ),
                ]
            ),
            StructureExtractor(
                name="Pistil",
                pattern=r"pistils\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    NumericAttributeExtractor(
                        name="Count",
                        units=[]  # No units for count
                    ),
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
            NumericAttributeExtractor(
                name="Width",
                prefix_qualifiers=["generally", "mostly", "usually"],
                units=["mm", "cm"]
            ),
            
            shape_extractor,
        ],
        child_extractors=[
            StructureExtractor(
                name="Sepal",
                pattern=r"sepals\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    erectness_extractor,
                    
                    QualitativeAttributeExtractor(
                        name="Persistence",
                        value_words=["persistent", "deciduous", "caducous"]
                    ),
                ]
            ),
            StructureExtractor(
                name="Achene",
                pattern=r"achenes\s+(.+?)(?=;|$)",
                attribute_extractors=[
                    NumericAttributeExtractor(
                        name="Size",
                        prefix_qualifiers=["generally", "mostly", "usually"],
                        allow_decimal=True,
                        units=["mm", "cm"]
                    ),
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
