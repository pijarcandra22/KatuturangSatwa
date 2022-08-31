import re

class DisambiguatorBaliPrefixRule6a(object):
    """Disambiguate Prefix Rule 6a
    Rule 6a : kaV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^ka([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule6b(object):
    """Disambiguate Prefix Rule 6b
    Rule 6b : kV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^k([aiueo].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule6c(object):
    """Disambiguate Prefix Rule 6c
    Rule 6c : koV -> uV
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^ko([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return 'u' + matches.group(1)


