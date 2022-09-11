import re

class DisambiguatorBaliWewehanRule17a(object):
    """Disambiguate Wewehan Rule 17a
    Rule 17a : kaVan -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^ka([aiueobcdfghjklmnpqrstvwxyz].*)an$', word)
        if matches:
            return matches.group(1)

