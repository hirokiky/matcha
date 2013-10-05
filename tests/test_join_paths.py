import pytest


@pytest.fixture
def target():
    from matcha import join_paths
    return join_paths


def test_join_paths(target):
    assert target('/mio/', '/ritsu/') == '/mio/ritsu/'
