import re

class DisambiguatorBaliSuffixRule21a(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueo])n$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule21b(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])in$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule21c(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueo])nin$', word)
        if matches:
            return matches.group(1)
class DisambiguatorBaliSuffixRule21d(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])nan$', word)
        if matches:
            return matches.group(1)



