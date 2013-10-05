import pytest


@pytest.fixture
def target():
    from matcha import make_wsgi_app
    return make_wsgi_app


def dummy_case(environ, start_response):
    return environ, start_response


def dummy_matching(environ):
    return dummy_case, 'dummy_matched_dict'


def dummy_not_matched_app(environ, start_response):
    return 'not matched'


def dummy_matching_not_matched(environ):
    from matcha import NotMatched
    raise NotMatched


def test_matched(target):
    inner_target = target(dummy_matching)

    dummy_environ = {}
    actual = inner_target(dummy_environ, 'dummy_start_response')

    assert dummy_environ['matcha.matched_dict'] == 'dummy_matched_dict'
    assert dummy_environ['matcha.matching'] == dummy_matching
    assert actual == (dummy_environ, 'dummy_start_response')


def test_not_matched(target):
    inner_target = target(dummy_matching_not_matched,
                          not_found_app=dummy_not_matched_app)

    dummy_environ = {}
    actual = inner_target(dummy_environ, 'dummy_start_response')

    assert actual == 'not matched'
    assert dummy_environ['matcha.matching'] == dummy_matching_not_matched
