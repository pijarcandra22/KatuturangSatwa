import re

class DisambiguatorBaliSeselanRule14a(object):
    """Disambiguate Seselan Rule 14a
    Rule 14a : X-er-V -> XV
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^([bcdfghjklmnpqrstvwxyz])er([aiueo].*)$', word)
        if matches:
            return matches.group(1) + matches.group(2)

class DisambiguatorBaliSeselanRule14b(object):
    """Disambiguate Seselan Rule 14b
    Rule 14a : X-el-V -> XV
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^([bcdfghjklmnpqrstvwxyz])el([aiueo].*)$', word)
        if matches:
            return matches.group(1) + matches.group(2)

