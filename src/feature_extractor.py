import re
import logging
from src.feature_node import FeatureNode
from src.feature_value import FeatureValue

# Configure logging in the test or main
logger = logging.getLogger(__name__)

def _clean_value(val):
    return val.rstrip('.').strip()

class FeatureExtractor:
    def __init__(self, name: str, pattern=None, children=None):
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE) if isinstance(pattern, str) else pattern
        self.children = children or []

    def get_match_range(self, text):
        if self.pattern is not None:
            m = self.pattern.search(text)
            if m and m.lastindex and m.group(1).strip():
                start, end = m.start(0), m.end(0)
                logger.debug(f"get_match_range: {self.name} found match at ({start}, {end}) in {repr(text)}")
                return (start, end)
            else:
                logger.debug(f"get_match_range: {self.name} no match or empty group in {repr(text)}")
                return (-1, -1)
        elif self.children:
            child_ranges = [child.get_match_range(text) for child in self.children]
            valid = [r for r in child_ranges if r[0] != -1]
            if not valid:
                logger.debug(f"get_match_range: {self.name} no children matched in {repr(text)}")
                return (-1, -1)
            start = min(r[0] for r in valid)
            end = max(r[1] for r in valid)
            logger.debug(f"get_match_range: {self.name} container range ({start}, {end}) in {repr(text)}")
            return (start, end)
        else:
            logger.debug(f"get_match_range: {self.name} no pattern, no children in {repr(text)}")
            return (-1, -1)

    def extract(self, text):
        logger.debug(f"Entering extract: name={self.name}, pattern={getattr(self.pattern, 'pattern', None)}, text={repr(text)}")
        if not self.children:
            return self._extract_leaf_node(text)
        else:
            return self._extract_internal_node(text)

    def _extract_leaf_node(self, text):
        if self.pattern is not None:
            m = self.pattern.search(text)
            logger.debug(f"Leaf node {self.name}: pattern match={bool(m)}")
            if m and m.lastindex and m.group(1).strip():
                raw_value = m.group(1).strip()
                logger.debug(f"Leaf node {self.name}: captured group value={repr(raw_value)}")

                # Split on range and value delimiters
                # e.g. '8--25 dm', 'shrub or thicket-forming', 'red, green'
                # For now, only basic splitting; qualifiers handled later
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

                return FeatureNode(self.name, values=values)
            else:
                logger.debug(f"Leaf node {self.name}: no match or empty group, skipping node")
                return None
        else:
            logger.debug(f"Leaf node {self.name}: no pattern, skipping node")
            return None

    def _extract_internal_node(self, text):
        # Get match ranges for all children
        child_infos = []
        for child in self.children:
            start, end = child.get_match_range(text)
            if start != -1:
                child_infos.append({'child': child, 'start': start, 'end': end})
        if not child_infos:
            logger.debug(f"No children matched for {self.name}; returning None")
            return None
        # Sort by start
        child_infos.sort(key=lambda x: x['start'])
        # Truncate ends at next start
        for i in range(len(child_infos) - 1):
            child_infos[i]['end'] = min(child_infos[i]['end'], child_infos[i+1]['start'])
        # Extract children
        nodes = []
        for info in child_infos:
            # Pass the full matched substring (including the label) to the child
            child_text = text[info['start']:info['end']]
            logger.debug(f"Passing region to child '{info['child'].name}': {repr(child_text)}")
            child_node = info['child'].extract(child_text)
            if child_node:
                logger.debug(f"Child node created: {child_node.name} (value={getattr(child_node, 'value', None)})")
                nodes.append(child_node)
        if nodes:
            node = FeatureNode(self.name)
            for n in nodes:
                node.add_child(n)
            logger.debug(f"Created node: {node.name} with {len(nodes)} children")
            return node
        else:
            logger.debug(f"No children nodes created for {self.name}; returning None")
            return None
