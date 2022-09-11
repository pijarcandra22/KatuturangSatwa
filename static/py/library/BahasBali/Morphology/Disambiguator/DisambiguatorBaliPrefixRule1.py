import re

class DisambiguatorBaliPrefixRule1a(object):
    """Disambiguate Prefix Rule 1a
    Rule 1a : ngV -> V
    """

    def disambiguate(self, word):
        """Disambiguate Prefix Rule 1a
        Rule 1a : ngV -> V
        """
        matches = re.match(r'^ng([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule1b(object):
    """Disambiguate Prefix Rule 1b
    Rule 1b : ngV -> kV
    """

    def disambiguate(self, word):
        #print(word)
        """Disambiguate Prefix Rule 1b
        Rule 1b : ngV -> kV
        """
        matches = re.match(r'^ng([aiueo].*)$', word)
        if matches:
            return 'k' + matches.group(1)


class DisambiguatorBaliPrefixRule1c(object):
    """Disambiguate Prefix Rule 1b
    Rule 1b : ngV -> gV
    """

    def disambiguate(self, word):
        # print(word)
        """Disambiguate Prefix Rule 1b
        Rule 1b : ngV -> gV
        """
        matches = re.match(r'^ng([aiueo].*)$', word)
        if matches:
            return 'g' + matches.group(1)

class DisambiguatorBaliPrefixRule1d(object):
    """Disambiguate Prefix Rule 1d
    Rule 5a : ngaV-> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^nga([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule1e(object):
    """Disambiguate Prefix Rule 1e
    Rule 1e : ngeV-> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^nge([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
