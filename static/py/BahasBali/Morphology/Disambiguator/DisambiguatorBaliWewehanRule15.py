import re

class DisambiguatorBaliWewehanRule15a(object):
    """Disambiguate Wewehan Rule 15a
    Rule 14a : maVan -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^ma([aiueobcdfghjklmnpqrstvwxyz].*)an$', word)
        if matches:
            return matches.group(1)

