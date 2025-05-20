from src.feature_extractor import FeatureExtractor


def test_feature_extractor_basic():
    # Simple pattern: Section: value
    matcher = FeatureExtractor(
        name='HelloWorld',
        pattern=r'^Hello world!'
    )
    text = 'Hello world!'
    node = matcher.extract(text)
    assert node.name == 'HelloWorld'
    assert node.value == 'Hello world!'


def test_feature_extractor_split():
    # Test splitting
    matcher = FeatureExtractor(
        name='Root',
        pattern=r'.*',
        children=[
            FeatureExtractor(
                name='Item1',
                pattern=r'Item1:',
                consume_pattern=True
            ),
            FeatureExtractor(
                name='Item2',
                pattern=r'Item2:',
                consume_pattern=True
            ),
            FeatureExtractor(
                name='Item3',
                pattern=r'Item3:',
                consume_pattern=True
            ),
        ],
        split=r';'
    )
    text = 'Item1: apple; Item2: banana; Item3: cherry'
    node = matcher.extract(text)
    assert node.name == 'Root'
    assert len(node.children) == 3
    assert {(c.name, c.value) for c in node.children} \
        == {('Item1', 'apple'), ('Item2', 'banana'), ('Item3', 'cherry')}
