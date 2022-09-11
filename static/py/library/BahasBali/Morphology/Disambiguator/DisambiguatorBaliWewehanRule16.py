import re

class DisambiguatorBaliWewehanRule16a(object):
    """Disambiguate Wewehan Rule 16a
    Rule 16a : paVan -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^pa([aiueobcdfghjklmnpqrstvwxyz].*)an$', word)
        if matches:
            return matches.group(1)

