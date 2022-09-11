import re

class DisambiguatorBaliWewehanRule18a(object):
    """Disambiguate Wewehan Rule 18a
    Rule 18a : braVan -> V
    """

    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^bra([aiueobcdfghjklmnpqrstvwxyz].*)an$', word)
        if matches:
            return matches.group(1)

