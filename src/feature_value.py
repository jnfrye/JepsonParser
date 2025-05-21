from typing import Optional, List

class FeatureValue:
    """
    Represents a value (or a range endpoint) for a feature in a taxonomic description.
    If is_range_start is True, this value is the start of a range that ends at the next value in the list.
    """
    def __init__(self, raw_value: str, qualifier: Optional[str] = None, is_range_start: bool = False):
        self.raw_value = raw_value
        self.qualifier = qualifier
        self.is_range_start = is_range_start

    def __repr__(self):
        return f"FeatureValue(raw_value={self.raw_value!r}, qualifier={self.qualifier!r}, is_range_start={self.is_range_start})"

def split_feature_values(raw_value: str) -> List[FeatureValue]:
    """
    Splits a raw feature value string into a list of FeatureValue objects, handling ranges and multi-values.
    For now, only basic splitting and range detection; qualifiers handled later.
    """
    values = []
    delimiters = [('--', True), (' to ', True), (' or ', False), (',', False)]
    splits = [(d, is_range) for d, is_range in delimiters if d in raw_value]
    if splits:
        # Use the first matching delimiter
        delim, is_range = splits[0]
        parts = [p.strip() for p in raw_value.split(delim)]
        for i, part in enumerate(parts):
            values.append(FeatureValue(
                raw_value=part,
                qualifier=None,
                is_range_start=(is_range and i == 0)
            ))
    else:
        values.append(FeatureValue(raw_value=raw_value, qualifier=None, is_range_start=False))
    return values
