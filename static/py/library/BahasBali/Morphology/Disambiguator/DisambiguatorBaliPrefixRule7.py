import re

class DisambiguatorBaliPrefixRule7a(object):
    """Disambiguate Prefix Rule 7a
    Rule 7a : saV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^sa([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
