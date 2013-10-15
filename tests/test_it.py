from matcha import Matching as m
from matcha import include, bundle


about_pages = bundle(
    m('/htt/', 'htt', 'about_htt'),
    m('/activity/*activity', 'activity', 'about_activity')
)

member_pages = bundle(
    m('/', 'member_list', 'member_list'),
    m('/{member}/', 'member_detail', 'member_detail'),
)

matching = bundle(
    m('/', 'home', 'home'),
    include('/about/', about_pages),
    include('/member/', member_pages),
)


def test_it():
    assert matching['/'] == ('home', {})
    assert matching['/about/htt/'] == ('htt', {})
    assert matching['/about/activity/outdoor_fes/2013/winter'] == \
        ('activity', {'activity': ['outdoor_fes', '2013', 'winter']})
    assert matching['/member/'] == ('member_list', {})
    assert matching['/member/ritsu/'] == ('member_detail', {'member': 'ritsu'})
