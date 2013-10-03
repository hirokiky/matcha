import pytest


@pytest.fixture
def target_class():
    from matcha import Matching
    return Matching


class DummyPatternTemplate(object):
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, path_info):
        self.called_with = path_info
        return self.return_value


def get_matching_records(pattern_tamplate, case, name):
    from matcha import MatchingRecord
    return [MatchingRecord(pattern_tamplate, case, name)]


def test_getitem(target_class):
    dummy_pattern_template = DummyPatternTemplate({'dummy': 'matched_dict'})
    dummy_matching_records = get_matching_records(dummy_pattern_template, 'dummy_case', '')

    target = target_class(matching_records=dummy_matching_records)
    actual = target['path_info']

    assert actual[0] == 'dummy_case'
    assert actual[1] == {'dummy': 'matched_dict'}
    assert dummy_pattern_template.called_with == 'path_info'


def test_getitem_not_matched(target_class):
    from matcha import NotMatched
    dummy_pattern_template = DummyPatternTemplate(None)
    dummy_matching_records = get_matching_records(dummy_pattern_template, '', '')

    target = target_class(matching_records=dummy_matching_records)

    with pytest.raises(NotMatched):
        target['path_info']
    assert dummy_pattern_template.called_with == 'path_info'
