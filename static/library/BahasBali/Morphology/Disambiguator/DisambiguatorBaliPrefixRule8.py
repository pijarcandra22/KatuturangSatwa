import re

class DisambiguatorBaliPrefixRule8a(object):
    """Disambiguate Prefix Rule 8a
    Rule 8a : patV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pat([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8b(object):
    """Disambiguate Prefix Rule 8b
    Rule 8b : pakV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pak([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8c(object):
    """Disambiguate Prefix Rule 8c
    Rule 8c : pikV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pik([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8d(object):
    """Disambiguate Prefix Rule 8d
    Rule 8d : piV -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pi([aiueo].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8e(object):
    """Disambiguate Prefix Rule 8e
        Rule 8e : patiV -> V
        """

    def disambiguate(self, word):
        # print(word)
        matches = re.match(r'^pati([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8f(object):
    """Disambiguate Prefix Rule 8e
    Rule 8e : pariV -> V
    """
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pari([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliPrefixRule8g(object):
    """Disambiguate Prefix Rule 8e
        Rule 8e : paV -> V
        """

    def disambiguate(self, word):
        # print(word)
        matches = re.match(r'^pa([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)

