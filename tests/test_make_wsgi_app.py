import pytest


@pytest.fixture
def target():
    from matcha import make_wsgi_app
    return make_wsgi_app


def dummy_case(environ, start_response):
    return environ, start_response


def dummy_matching(environ):
    return dummy_case


def test_make_wsgi_app(target):
    inner_target = target(dummy_matching)

    actual = inner_target('dummy_environ', 'dummy_start_response')

    assert actual[0] == 'dummy_environ'
    assert actual[1] == 'dummy_start_response'
