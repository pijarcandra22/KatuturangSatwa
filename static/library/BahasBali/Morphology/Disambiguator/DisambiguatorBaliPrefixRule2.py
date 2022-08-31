import re

class DisambiguatorBaliPrefixRule2a(object):
    """Disambiguate Prefix Rule 1a
    Rule 1a : nyV -> V
    """

    def disambiguate(self, word):
        """Disambiguate Prefix Rule 1a
        Rule 1a : nyV -> V
        """
        matches = re.match(r'^ny([aiueokgyrl].*)$', word)
        if matches:
            return 'c' + matches.group(1)

class DisambiguatorBaliPrefixRule2b(object):
    """Disambiguate Prefix Rule 1b
    Rule 2b : ngV -> kV
    """

    def disambiguate(self, word):
        """Disambiguate Prefix Rule 2b
        Rule 2b : ngV -> kV
        """
        matches = re.match(r'^ny([aiueo].*)$', word)
        if matches:
            return 'j' + matches.group(1)


class DisambiguatorBaliPrefixRule2c(object):
    """Disambiguate Prefix Rule 1b
    Rule 2c : ngV -> gV
    """

    def disambiguate(self, word):
        """Disambiguate Prefix Rule 1b
        Rule 2c : ngV -> gV
        """
        matches = re.match(r'^ny([aiueo].*)$', word)
        if matches:
            return 's' + matches.group(1)
