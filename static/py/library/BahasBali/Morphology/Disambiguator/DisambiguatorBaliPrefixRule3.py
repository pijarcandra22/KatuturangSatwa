import re

class DisambiguatorBaliPrefixRule3a(object):
    """Disambiguate Prefix Rule 3a
    Rule 3a : nV -> tV
    """

    def disambiguate(self, word):
        matches = re.match(r'^n([aiueo].*)$', word)
        if matches:
            return 't' + matches.group(1)

class DisambiguatorBaliPrefixRule3b(object):
    """Disambiguate Prefix Rule 3b
    Rule 3b : nV -> dV
    """

    def disambiguate(self, word):
        matches = re.match(r'^n([aiueo].*)$', word)
        if matches:
            return 'd' + matches.group(1)

