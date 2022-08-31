import re

class DisambiguatorBaliPrefixRule5a(object):
    """Disambiguate Prefix Rule 5a
    Rule 5a : ngaV(rule1)-> gaV -> V
    """

    def disambiguate(self, word):
        print(word)
        matches = re.match(r'^ga([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule5b(object):
    """Disambiguate Prefix Rule 5b
    Rule 5b : ngeV(rule1)-> geV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^ge([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)


