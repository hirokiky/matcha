from matcha import Matching as m
from matcha import include, bundle


about_pages = bundle(
    m('/htt/', 'htt', 'htt'),
)

member_pages = bundle(
    m('/', 'member_list', 'list'),
    m('/{member}/', 'member_detail', 'detail'),
)

dispatcher = bundle(
    m('/', 'home', 'home'),
    include('/about/', about_pages, 'about'),
    include('/member/', member_pages, 'member'),
)


def test_it():
    assert dispatcher['/'] == ('home', {})
    assert dispatcher['/about/htt/'] == ('htt', {})
    assert dispatcher['/member/'] == ('member_list', {})
    assert dispatcher['/member/ritsu/'] == ('member_detail', {'member': 'ritsu'})
