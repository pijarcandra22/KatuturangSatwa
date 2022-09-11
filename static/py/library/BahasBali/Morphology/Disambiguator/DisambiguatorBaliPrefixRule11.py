import re

class DisambiguatorBaliPrefixRule11a(object):
    """Disambiguate Prefix Rule 11a
    Rule 11a : kumaV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^kuma([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
