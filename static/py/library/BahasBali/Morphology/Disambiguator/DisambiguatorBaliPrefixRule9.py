import re

class DisambiguatorBaliPrefixRule9a(object):
    """Disambiguate Prefix Rule 9a
    Rule 9a : aV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^a([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
