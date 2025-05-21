from src.feature_value import split_feature_values

from src.feature_value import split_feature_values

def test_single_value():
    values = split_feature_values('red')
    assert len(values) == 1
    assert values[0].raw_value == 'red'
    assert not values[0].is_range_start
    assert values[0].unit is None

def test_single_numeric_with_unit():
    values = split_feature_values('15 mm')
    assert len(values) == 1
    assert values[0].raw_value == '15'
    assert not values[0].is_range_start
    assert values[0].unit == 'mm'

def test_range_value():
    values = split_feature_values('8--25 dm')
    assert len(values) == 2
    assert values[0].raw_value == '8'
    assert values[0].is_range_start
    assert values[0].unit == 'dm'
    assert values[1].raw_value == '25'
    assert not values[1].is_range_start
    assert values[1].unit == 'dm'

def test_or_value():
    values = split_feature_values('shrub or thicket-forming')
    assert len(values) == 2
    assert values[0].raw_value == 'shrub'
    assert not values[0].is_range_start
    assert values[0].unit is None
    assert values[1].raw_value == 'thicket-forming'
    assert not values[1].is_range_start
    assert values[1].unit is None

def test_comma_value():
    values = split_feature_values('red, green, blue')
    assert len(values) == 3
    assert [v.raw_value for v in values] == ['red', 'green', 'blue']
    assert all(not v.is_range_start for v in values)
    assert all(v.unit is None for v in values)

def test_to_range():
    values = split_feature_values('2 to 5 mm')
    assert len(values) == 2
    assert values[0].raw_value == '2'
    assert values[0].is_range_start
    assert values[0].unit == 'mm'
    assert values[1].raw_value == '5'
    assert not values[1].is_range_start
    assert values[1].unit == 'mm'
