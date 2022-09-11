import re

class DisambiguatorBaliSuffixRule20a(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])a$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule20b(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueo])na$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule20c(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])ina$', word)
        if matches:
            return matches.group(1)
class DisambiguatorBaliSuffixRule20d(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])ng$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule20e(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^da([aiueobcdfghjklmnpqrstvwxyz].*)$', word)
        if matches:
            return matches.group(1)



