import pytest
import webtest


def create_dummy_wsgi_app(body):
    def dummy_wsgi_app(environ, start_response):
        headers = [('Content-Type', 'text/html; charset=utf8'),
                   ('Content-Length', str(len(body)))]
        start_response('200 Ok', headers)
        return [body]
    return dummy_wsgi_app


about_htt_app = create_dummy_wsgi_app(
    b"Ho-Kago Tea Time is a Light Music Club"
    b" to five Sakuragaoka High School students belong"
)


@pytest.fixture
def target():
    from matcha import Matching, make_wsgi_app
    wsgi_app = make_wsgi_app(Matching('/about/', about_htt_app))
    return webtest.TestApp(wsgi_app)


def test_ft(target):
    resp = target.get('/about/')
    assert resp.status == '200 Ok'
    assert b"Ho-Kago Tea Time is a" in resp.body
