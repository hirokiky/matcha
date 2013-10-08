from collections import namedtuple


class NotMatched(Exception):
    """ Exception class for telling the matching was failed
    """


class NotReversed(Exception):
    """ Exception class for telling the reversing was failed
    """


MatchingRecord = namedtuple('MatchingRecord', 'path_template case name')


class Matching(object):
    def __init__(self, pattern='', case='', name='', matching_records=()):
        if matching_records:
            self.matching_records = matching_records
        else:
            self.matching_records = [MatchingRecord(PathTemplate(pattern), case, (name,))]

    def __call__(self, environ):
        """ Getting environ and return a matched case and a URL kwargs.
        """
        path_info = environ['PATH_INFO']
        script_name = environ['SCRIPT_NAME']

        record, path_matched = self._scanning_matching_records(path_info)

        try:
            extra_index = index_repeatedly(path_info, '/', path_matched.matched_index)
        except ValueError:
            extra_index = len(path_info)

        environ['PATH_INFO'] = path_info[extra_index:]
        environ['SCRIPT_NAME'] = join_paths(script_name, path_info[:extra_index])

        return record.case, path_matched.matched_dict

    def __getitem__(self, path_info):
        """ Getting a PATH_INFO and return a matched case and a URL kwargs
        """
        record, path_matched = self._scanning_matching_records(path_info)
        return record.case, path_matched.matched_dict

    def _scanning_matching_records(self, path_info):
        for record in self.matching_records:
            path_matched = record.path_template(path_info)
            if path_matched is None:
                continue
            else:
                break
        else:
            raise NotMatched
        return record, path_matched

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
                path_template = record.path_template
                break
        else:
            raise NotReversed

        if path_template.wildcard_name:
            l = kwargs.get(path_template.wildcard_name)
            if not l:
                raise NotReversed
            additional_path = '/'.join(l)
            extra_path_elements = path_template.pattern.split('/')[:-1]
            pattern = join_paths('/'.join(extra_path_elements), additional_path)
        else:
            pattern = path_template.pattern

        try:
            url = pattern.format(**kwargs)
        except KeyError:
            raise NotReversed
        return url


PathMatched = namedtuple('PathMatched', 'matched_index matched_dict')


class PathTemplate(object):
    def __init__(self, pattern):
        self.pattern = pattern

        last_pattern_element = self.pattern.split('/')[-1]
        if last_pattern_element.startswith('*'):
            self.wildcard_name = last_pattern_element[1:]
        else:
            self.wildcard_name = None

    def __call__(self, path_info):
        pattern_elements = self.pattern.split('/')
        path_elements = path_info.split('/')

        matched_dict = {}

        if self.wildcard_name:
            matched_index = len(pattern_elements) - 1
            matched_dict[self.wildcard_name] = path_elements[matched_index:]
            path_elements = path_elements[:matched_index]
            pattern_elements = pattern_elements[:-1]
        else:
            matched_index = len(path_elements)

        if len(pattern_elements) != len(path_elements):
            return None

        for patt, path in zip(pattern_elements, path_elements):
            if patt.startswith('{') and patt.endswith('}'):
                key = patt.strip('{}')
                matched_dict[key] = path
            elif patt != path:
                return None

        return PathMatched(matched_index, matched_dict)

    def __add__(self, other):
        return self.__class__(join_paths(self.pattern, other.pattern))

    def __repr__(self):
        return "<matcha.PathTemplate pattern:'{0}'>".format(self.pattern)


def join_paths(left_path, right_path):
    return left_path.rstrip('/') + '/' + right_path.lstrip('/')


def index_repeatedly(s, sub, times):
    i = -1
    for _ in range(times):
        i += 1
        i = s.index(sub, i)
    return i


def bundle(*addable):
    """ Getting addable objects (such as Matching) and composing them to one.
    When nothing is provided, this will raise a ValueError
    """
    if len(addable) <= 0:
        raise ValueError('Provide at least one Matching object')
    return sum(addable[1:], addable[0])


def include(pattern, matching, name=''):
    """ Including a other matching, to get as matching pattern's child paths.
    """
    matching.matching_records = [
        MatchingRecord(
            PathTemplate(pattern) + child_path_template,
            case,
            (name,) + child_name
        ) for child_path_template, case, child_name in matching.matching_records
    ]
    return matching


def not_found_app(environ, start_response):
    start_response('404 Not Found', [('content-type', 'text/plain')])
    return [b'Requested URL was not found on this server.']


def make_wsgi_app(matching, not_found_app=not_found_app):
    """ Making a WSGI application from Matching object
    registered other WSGI applications on each 'case' argument.
    """
    def wsgi_app(environ, start_response):
        environ['matcha.matching'] = matching
        try:
            matched_case, matched_dict = matching(environ)
        except NotMatched:
            return not_found_app(environ, start_response)
        else:
            environ['matcha.matched_dict'] = matched_dict
            return matched_case(environ, start_response)
    return wsgi_app
