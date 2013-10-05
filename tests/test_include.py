import pytest


@pytest.fixture
def target():
    from matcha import include
    return include


@pytest.fixture
def matching():
    from matcha import Matching
    return Matching('/child', 'case', 'child')


def test_with_one_child(target, matching):
    actual = target('/parent', matching, 'parent')

    assert len(actual.matching_records) == 1
    assert actual.matching_records[0].path_template.pattern == '/parent/child'
    assert actual.matching_records[0].case == 'case'
    assert actual.matching_records[0].name == ('parent', 'child')
