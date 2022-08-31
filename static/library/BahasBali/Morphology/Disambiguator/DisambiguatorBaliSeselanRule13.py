import re

class DisambiguatorBaliSeselanRule13a(object):
    """Disambiguate Seselan Rule 13a
    Rule 13a : X-um-V -> XV
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^([bcdfghjklmnpqrstvwxyz])um([aiueo].*)$', word)
        if matches:
            return matches.group(1) + matches.group(2)

