import re

class DisambiguatorBaliPrefixRule10a(object):
    """Disambiguate Prefix Rule 10a
    Rule 10a : praV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pra([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)
