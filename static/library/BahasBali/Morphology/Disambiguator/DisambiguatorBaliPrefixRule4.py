import re

class DisambiguatorBaliPrefixRule4a(object):
    """Disambiguate Prefix Rule 4d
        Rule 4d : mV -> bV
        """

    def disambiguate(self, word):
        matches = re.match(r'^m([aiueo].*)$', word)
        if matches:
            return 'b' + matches.group(1)

class DisambiguatorBaliPrefixRule4b(object):
    """Disambiguate Prefix Rule 4b
    Rule 4b : mamV -> V
    """

    def disambiguate(self, word):
        matches = re.match(r'^mam([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
class DisambiguatorBaliPrefixRule4c(object):
    """Disambiguate Prefix Rule 4c
    Rule 4c : mamV -> pV
    """

    def disambiguate(self, word):
        matches = re.match(r'^mam([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return 'p' + matches.group(1)
class DisambiguatorBaliPrefixRule4d(object):
    """Disambiguate Prefix Rule 4b
    Rule 4b : mV -> V
    """

    def disambiguate(self, word):
        matches = re.match(r'^mam([aiueo].*)$', word)
        if matches:
            return 'b' + matches.group(1)

class DisambiguatorBaliPrefixRule4e(object):
    """Disambiguate Prefix Rule 4b
    Rule 4b : mV -> V
    """

    def disambiguate(self, word):
        matches = re.match(r'^m([aiueo].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule4f(object):
    """Disambiguate Prefix Rule 4c
    Rule 4c : mV -> pV
    """

    def disambiguate(self, word):
        matches = re.match(r'^m([aiueo].*)$', word)
        if matches:
            return 'p' + matches.group(1)

class DisambiguatorBaliPrefixRule4g(object):
    """Disambiguate Prefix Rule 4a
        Rule 4a : maV -> V
        """

    def disambiguate(self, word):
        matches = re.match(r'^ma([bcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

