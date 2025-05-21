from src.feature_extractor import FeatureExtractor


def test_feature_extractor_basic():
    # Simple pattern: Section: value
    matcher = FeatureExtractor(
        name='HelloWorld',
        pattern=r'Hello:\s*(.+)'
    )
    text = 'Hello: world!'
    node = matcher.extract(text)
    assert node.name == 'HelloWorld'
    assert node.value == 'world!'


def test_feature_extractor_split():
    # Test splitting
    color_matcher = FeatureExtractor(
        name='Color',
        pattern=r'(red|green)'
    )
    matcher = FeatureExtractor(
        name='Root',
        pattern=r'(.+)',
        children=[
            FeatureExtractor(
                name='Item1',
                pattern=r'Item1:\s*(.+)',
                children=[color_matcher]
            ),
            FeatureExtractor(
                name='Item2',
                pattern=r'; Item2:\s*(.+)',
                children=[color_matcher]
            ),
        ]
    )
    text = 'Item1: apple red; Item2: apple green'
    node = matcher.extract(text)
    assert node.name == 'Root'
    assert len(node.children) == 2
    assert {(c.name, c.value) for c in node.children} \
        == {('Item1', None), ('Item2', None)}
    assert {(c.name, c.value) for c in node.children[0].children} \
        == {('Color', 'red')}
    assert {(c.name, c.value) for c in node.children[1].children} \
        == {('Color', 'green')}

def test_get_match_range_basic():
    fe = FeatureExtractor(name='Test', pattern=r'foo: (\w+)')
    text = 'foo: bar'
    start, end = fe.get_match_range(text)
    # Should match 'foo: bar' in 'foo: bar' (entire match)
    assert text[start:end] == 'foo: bar'


def test_get_match_range_no_match():
    fe = FeatureExtractor(name='Test', pattern=r'foo: (\w+)')
    text = 'baz: bar'
    start, end = fe.get_match_range(text)
    assert (start, end) == (-1, -1)


def test_get_match_range_empty_group():
    fe = FeatureExtractor(name='Test', pattern=r'foo: (\w*)')
    text = 'foo: '
    start, end = fe.get_match_range(text)
    # Group exists, but is empty/whitespace
    assert (start, end) == (-1, -1)


def test_get_match_range_with_children():
    child1 = FeatureExtractor(name='Child1', pattern=r'A: (\d+)')
    child2 = FeatureExtractor(name='Child2', pattern=r'B: (\d+)')
    parent = FeatureExtractor(name='Parent', children=[child1, child2])
    text = 'A: 10; B: 20'
    start, end = parent.get_match_range(text)
    # Should span from start of 'A: 10' to end of 'B: 20' (entire matches)
    assert text[start:end] == 'A: 10; B: 20'


def test_get_match_range_children_no_match():
    child1 = FeatureExtractor(name='Child1', pattern=r'A: (\d+)')
    child2 = FeatureExtractor(name='Child2', pattern=r'B: (\d+)')
    parent = FeatureExtractor(name='Parent', children=[child1, child2])
    text = 'C: 30'
    start, end = parent.get_match_range(text)
    assert (start, end) == (-1, -1)

    # Test splitting
    color_matcher = FeatureExtractor(
                        name='Color',
                        pattern=r'(red|green)'
                    )
    matcher = FeatureExtractor(
        name='Root',
        pattern=r'(.+)',
        children=[
            FeatureExtractor(
                name='Item1',
                pattern=r'Item1:\s*(.+)',
                children=[color_matcher]
            ),
            FeatureExtractor(
                name='Item2',
                pattern=r'; Item2:\s*(.+)',
                children=[color_matcher]
            ),
        ]
    )
    text = 'Item1: apple red; Item2: apple green'
    node = matcher.extract(text)
    assert node.name == 'Root'
    assert len(node.children) == 2
    assert {(c.name, c.value) for c in node.children} \
        == {('Item1', None), ('Item2', None)}
    assert {(c.name, c.value) for c in node.children[0].children} \
        == {('Color', 'red')}
    assert {(c.name, c.value) for c in node.children[1].children} \
        == {('Color', 'green')}

def test__extract_leaf_node_basic():
    # Should extract value from leaf node with pattern
    fe = FeatureExtractor(name='Leaf', pattern=r'Leaf: (.+)')
    text = 'Leaf: simple-value'
    node = fe._extract_leaf_node(text)
    assert node is not None
    assert node.name == 'Leaf'
    assert node.value == 'simple-value'

def test__extract_leaf_node_no_match():
    # Should return None if pattern does not match
    fe = FeatureExtractor(name='Leaf', pattern=r'Leaf: (.+)')
    text = 'Stem: not-a-leaf'
    node = fe._extract_leaf_node(text)
    assert node is None

def test__extract_leaf_node_empty_group():
    # Should return None if group is empty
    fe = FeatureExtractor(name='Leaf', pattern=r'Leaf: (.*)')
    text = 'Leaf: '
    node = fe._extract_leaf_node(text)
    assert node is None

def test__extract_leaf_node_no_pattern():
    # Should return None if no pattern is set
    fe = FeatureExtractor(name='Leaf')
    text = 'Leaf: something'
    node = fe._extract_leaf_node(text)
    assert node is None

def test__extract_internal_node_basic():
    # Should extract children from internal node
    child1 = FeatureExtractor(name='Child1', pattern=r'A: (\d+)')
    child2 = FeatureExtractor(name='Child2', pattern=r'B: (\d+)')
    parent = FeatureExtractor(name='Parent', children=[child1, child2])
    text = 'A: 10; B: 20'
    node = parent._extract_internal_node(text)
    assert node is not None
    assert node.name == 'Parent'
    assert len(node.children) == 2
    assert {c.name for c in node.children} == {'Child1', 'Child2'}

def test__extract_internal_node_no_children_match():
    # Should return None if no children match
    child1 = FeatureExtractor(name='Child1', pattern=r'A: (\d+)')
    child2 = FeatureExtractor(name='Child2', pattern=r'B: (\d+)')
    parent = FeatureExtractor(name='Parent', children=[child1, child2])
    text = 'C: 30'
    node = parent._extract_internal_node(text)
    assert node is None
