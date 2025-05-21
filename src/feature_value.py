from typing import Optional, List

import re
from typing import Optional, List

class FeatureValue:
    """
    Represents a value (or a range endpoint) for a feature in a taxonomic description.
    If is_range_start is True, this value is the start of a range that ends at the next value in the list.
    The 'unit' field captures measurement units (e.g., mm, cm, dm) for numeric values, or None for non-numeric values.
    """
    def __init__(self, raw_value: str, qualifier: Optional[str] = None, is_range_start: bool = False, unit: Optional[str] = None):
        self.raw_value = raw_value
        self.qualifier = qualifier
        self.is_range_start = is_range_start
        self.unit = unit

    def __repr__(self):
        return f"FeatureValue(raw_value={self.raw_value!r}, qualifier={self.qualifier!r}, is_range_start={self.is_range_start}, unit={self.unit!r})"

def split_feature_values(raw_value: str) -> List[FeatureValue]:
    """
    Splits a raw feature value string into a list of FeatureValue objects, handling ranges and multi-values.
    Extracts units for numeric values/ranges and assigns the unit to both start and end values if present.
    For non-numeric values, unit is None.
    """
    values = []
    delimiters = [('--', True), (' to ', True), (' or ', False), (',', False)]
    splits = [(d, is_range) for d, is_range in delimiters if d in raw_value]
    if splits:
        delim, is_range = splits[0]
        parts = [p.strip() for p in raw_value.split(delim)]
        # Try to extract unit from the last part
        unit = None
        unit_match = re.search(r"([\d.]+)\s*([a-zA-Zμ]+)$", parts[-1])
        if unit_match:
            unit = unit_match.group(2)
        for i, part in enumerate(parts):
            # Remove unit from the number if present (for start of range)
            if unit and re.match(r"^[\d.]+\s*" + re.escape(unit) + r"$", part):
                num = re.match(r"^[\d.]+", part).group(0)
                part_clean = num
            else:
                part_clean = part
            values.append(FeatureValue(
                raw_value=part_clean,
                qualifier=None,
                is_range_start=(is_range and i == 0),
                unit=unit
            ))
    else:
        # Try to extract unit if present
        unit = None
        unit_match = re.search(r"([\d.]+)\s*([a-zA-Zμ]+)$", raw_value)
        if unit_match:
            unit = unit_match.group(2)
            num = unit_match.group(1)
            raw_val_clean = num
        else:
            raw_val_clean = raw_value
        values.append(FeatureValue(raw_value=raw_val_clean, qualifier=None, is_range_start=False, unit=unit))
    return values
