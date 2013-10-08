import pytest


@pytest.fixture
def target():
    from matcha import index_repeatedly
    return index_repeatedly


def test_holded(target):
    assert target('/spam/ham/egg', '/', 3) == 9


def test_overflowed(target):
    with pytest.raises(ValueError):
        target('/spam/ham/egg', '/', 4)
