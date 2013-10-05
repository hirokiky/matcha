import pytest


@pytest.fixture
def target():
    from matcha import bundle
    return bundle


def test_without_args(target):
    with pytest.raises(ValueError):
        target()


def test_with_args(target):
    actual = target(['Ho-Kago'], ['Tea'], ['Time'])

    assert actual == ['Ho-Kago', 'Tea', 'Time']
