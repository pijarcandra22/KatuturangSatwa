import re

class DisambiguatorBaliSeselanRule12a(object):
    """Disambiguate Seselan Rule 12a
    Rule 12a : X-in-V -> XV
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^([bcdfghjklmnpqrstvwxyz])in([aiueo].*)$', word)
        if matches:
            return matches.group(1) + matches.group(2)

class DisambiguatorBaliSeselanRule12b(object):
    """Disambiguate Seselan Rule 12b
    Rule 12b : inV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^in([aiueo].*)$', word)
        if matches:
            return matches.group(1)
