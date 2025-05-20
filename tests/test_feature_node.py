from src.feature_node import FeatureNode

def test_feature_node_basic():
    node = FeatureNode('Root', 'rootval')
    child1 = FeatureNode('Child1', 'val1')
    child2 = FeatureNode('Child2', 'val2')
    node.add_child(child1)
    node.add_child(child2)

    assert node.name == 'Root'
    assert node.value == 'rootval'
    assert len(node.children) == 2
    assert node.children[0].name == 'Child1'
    assert node.children[1].value == 'val2'

    # Test find
    found = node.find('Child1')
    assert len(found) == 1
    assert found[0].value == 'val1'

    # Test to_dict
    d = node.to_dict()
    assert d['name'] == 'Root'
    assert d['children'][0]['name'] == 'Child1'
