from src.feature_extractor import FeatureExtractor

# Defines the schema for Habit features in Jepson descriptions

def get_habit_feature_schema():
    return FeatureExtractor(
        'Habit', r'Habit:\s*(.+)', [
            FeatureExtractor('General', None, [
                FeatureExtractor('Height', r'(\d+--\d+ ?[a-zA-Z]+)'),
                FeatureExtractor('Growth Form', r'((?:shrub|thicket-forming)(?:\sor\sthicket-forming)?)')
            ])
        ])

# Defines the schema for Stem features in Jepson descriptions

def get_stem_feature_schema():
    return FeatureExtractor(
        'Stem', r'Stem:\s*(.+)', [
            FeatureExtractor('Prickle', r'prickles\s*([^\.]+)', [
                FeatureExtractor('Count', r'(few[- ]to[- ]many|few|many)'),
                FeatureExtractor('Grouping', r'(paired[- ]or[- ]not|paired)'),
                FeatureExtractor('Length', r'(\d+--\d+ ?mm)'),
                FeatureExtractor('Shape', r'(thick-based[- ]and[- ]compressed|thick-based|compressed)'),
                FeatureExtractor('Curvature', r'(generally[- ]curved[- ]\(straight\)|curved|straight)'),
            ])
        ])

# Defines the schema for Leaf features in Jepson descriptions

def get_leaf_feature_schema():
    return FeatureExtractor(
        'Leaf', r'Leaf:\s*(.+)', [
            FeatureExtractor('Axis', r'axis\s*([^;]*)', [
                FeatureExtractor('Trichome', None, [
                    FeatureExtractor('Form', r'(shaggy-hairy|glabrous)'),
                    FeatureExtractor('Length', r'hairs to ([^,;]+)'),
                    FeatureExtractor('Glandularity', r'(glandless|glandular)')
                ])
            ])
        ])

# Defines the root schema for a Jepson taxon description

def get_jepson_feature_schema():
    return FeatureExtractor(
        'TaxonDescription', None, [
            get_habit_feature_schema(),
            get_stem_feature_schema(),
            get_leaf_feature_schema()
        ])
