from src.feature_node import FeatureNode
from src.feature_value import FeatureValue

def test_feature_node_basic():
    node = FeatureNode('Root', values=[FeatureValue(raw_value='rootval', qualifier=None, is_range_start=False)])
    child1 = FeatureNode('Child1', values=[FeatureValue(raw_value='val1', qualifier=None, is_range_start=False)])
    child2 = FeatureNode('Child2', values=[FeatureValue(raw_value='val2', qualifier=None, is_range_start=False)])
    node.add_child(child1)
    node.add_child(child2)

    assert node.name == 'Root'
    assert node.value == 'rootval'  # Backward compatibility
    assert node.values[0].raw_value == 'rootval'
    assert len(node.children) == 2
    assert node.children[0].name == 'Child1'
    assert node.children[1].value == 'val2'  # Backward compatibility
    assert node.children[1].values[0].raw_value == 'val2'

    # Test find
    found = node.find('Child1')
    assert len(found) == 1
    assert found[0].value == 'val1'  # Backward compatibility
    assert found[0].values[0].raw_value == 'val1'

    # Test to_dict
    d = node.to_dict()
    assert d['name'] == 'Root'
    assert d['children'][0]['name'] == 'Child1'
