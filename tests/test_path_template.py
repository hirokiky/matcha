import pytest


@pytest.fixture
def target_class():
    from matcha import PathTemplate
    return PathTemplate


def test_call_with_too_long_path(target_class):
    target = target_class('/instruments')

    assert target('/instruments/drums/1') is None


def test_call_not_matched(target_class):
    target = target_class('/instruments')

    assert target('/members') is None


def test_call_matched(target_class):
    target = target_class('/instruments/{instrument}')

    assert target('/instruments/drum') == {'instrument': 'drum'}


def test_add(target_class):
    target_left = target_class('/mio')
    target_right = target_class('/ritsu')

    actual = target_left + target_right

    assert actual.pattern == '/mio/ritsu'
