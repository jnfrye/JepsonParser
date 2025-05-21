from typing import Optional

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
