import pytest


@pytest.fixture
def target():
    from matcha import make_wsgi_app
    return make_wsgi_app


def dummy_case(environ, start_response):
    return environ, start_response


def dummy_matching(environ):
    return dummy_case, 'dummy_matched_dict'


def test_make_wsgi_app(target):
    inner_target = target(dummy_matching)

    dummy_environ = {}
    actual = inner_target(dummy_environ, 'dummy_start_response')

    assert dummy_environ['matcha.matched_dict'] == 'dummy_matched_dict'
    assert dummy_environ['matcha.matching'] == dummy_matching
    assert actual == (dummy_environ, 'dummy_start_response')
