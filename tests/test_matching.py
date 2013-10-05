import pytest


@pytest.fixture
def target_class():
    from matcha import Matching
    return Matching


def get_environ(environ={}):
    from wsgiref.util import setup_testing_defaults
    setup_testing_defaults(environ)
    return environ


class DummyPathTemplate(object):
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, path_info):
        self.called_with = path_info
        return self.return_value


def get_matching_records(path_tamplate, case, name):
    from matcha import MatchingRecord
    return [MatchingRecord(path_tamplate, case, name)]


def test_getitem(target_class):
    dummy_path_template = DummyPathTemplate({'dummy': 'matched_dict'})
    dummy_matching_records = get_matching_records(dummy_path_template, 'dummy_case', '')

    target = target_class(matching_records=dummy_matching_records)
    actual = target['path_info']

    assert actual[0] == 'dummy_case'
    assert actual[1] == {'dummy': 'matched_dict'}
    assert dummy_path_template.called_with == 'path_info'


def test_getitem_not_matched(target_class):
    from matcha import NotMatched
    dummy_path_template = DummyPathTemplate(None)
    dummy_matching_records = get_matching_records(dummy_path_template, '', '')

    target = target_class(matching_records=dummy_matching_records)

    with pytest.raises(NotMatched):
        target['path_info']
    assert dummy_path_template.called_with == 'path_info'


def test_call(target_class):
    target = target_class('/members/ritsu', 'dummy_case')
    environ = get_environ({'PATH_INFO': '/members/ritsu',
                           'SCRIPT_NAME': '/htt/'})

    actual = target(environ)

    assert actual[0] == 'dummy_case'
    assert actual[1] == {}
    assert environ['PATH_INFO'] == ''
    assert environ['SCRIPT_NAME'] == '/htt/members/ritsu'


def test_add(target_class):
    target1 = target_class(matching_records=['ritsu'])
    target2 = target_class(matching_records=['mio'])

    actual = target1 + target2

    assert actual.matching_records == ['ritsu', 'mio']


def test_reverse_matched(target_class):
    target = target_class('/members/{member}', 'dummy_case', 'member_detail')

    actual = target.reverse('member_detail', member='ritsu')

    assert actual == '/members/ritsu'


def test_reverse_not_matched(target_class):
    from matcha import NotReversed
    target = target_class('/members/ritsu', 'dummy_case', 'ritsu')

    with pytest.raises(NotReversed):
        target.reverse('mio')


def test_reverse_wrong_urlarg(target_class):
    from matcha import NotReversed
    target = target_class('/members/{member}', 'dummy_case', 'member_detail')

    with pytest.raises(NotReversed):
        target.reverse('member_detail', instrument='drum')
