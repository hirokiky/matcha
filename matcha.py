from collections import namedtuple


class NotMatched(Exception):
    """ Exception class for telling the matching was failed
    """


class NotReversed(Exception):
    """ Exception class for telling the reversing was failed
    """


MatchingRecord = namedtuple('MatchingRecord', 'pattern_template case name')


class Matching(object):
    def __init__(self, pattern='', case='', name='', matching_records=()):
        if matching_records:
            self.matching_records = matching_records
        else:
            self.matching_records = [MatchingRecord(PatternTemplate(pattern), case, (name,))]

    def __call__(self, environ):
        """ Getting environ and return a matched case and a URL kwargs.
        """
        path_info = environ['PATH_INFO']
        script_name = environ['SCRIPT_NAME']

        matched_case, matched_dict = self[path_info]

        environ['PATH_INFO'] = ''
        environ['SCRIPT_NAME'] = script_name.rstrip('/') + '/' + path_info.lstrip('/')

        return matched_case, matched_dict

    def __getitem__(self, path_info):
        """ Getting a PATH_INFO and return a matched case and a URL kwargs
        """
        for record in self.matching_records:
            matched_dict = record.pattern_template(path_info)
            if matched_dict is None:
                continue
            else:
                break
        else:
            raise NotMatched

        return record.case, matched_dict

    def __add__(self, other):
        """ Receiving a other Matching object and composing matching_records
        """
        composed_matching_records = self.matching_records + other.matching_records
        return self.__class__(matching_records=composed_matching_records)

    def reverse(self, *args, **kwargs):
        """ Getting a matching name and URL args and return a corresponded URL
        """
        for record in self.matching_records:
            if record.name == args:
                pattern_template = record.pattern_template
                break
        else:
            raise NotReversed
        try:
            url = pattern_template.pattern.format(**kwargs)
        except KeyError:
            raise NotReversed
        return url


class PatternTemplate(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, path_info):
        pattern_elements = self.pattern.split('/')
        path_elements = path_info.split('/')

        if len(pattern_elements) != len(path_elements):
            return None

        matched_dict = {}

        for patt, path in zip(pattern_elements, path_elements):
            if patt.startswith('{') and patt.endswith('}'):
                key = patt.strip('{}')
                matched_dict[key] = path
            elif patt != path:
                return None

        return matched_dict

    def __add__(self, other):
        return self.__class__(self.pattern + other.pattern)


def dispatcher(*matchings):
    """ Getting Matching objects and composing them to one Matching object.
    When nothing is provided, this will raise a ValueError
    """
    if len(matchings) <= 0:
        raise ValueError('Provide at least one Matching object')
    return sum(matchings[1:], matchings[0])


def include(pattern, matching, name=''):
    """ Including a other matching, to get as matching pattern's child paths.
    """
    matching.matching_records = [
        MatchingRecord(pattern + pattern, case, (name,) + child_name)
        for child_pattern, case, child_name in matching.matching_records
    ]
    return matching
