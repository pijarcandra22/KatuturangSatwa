import re

class DisambiguatorBaliSuffixRule19a(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])e$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule19b(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])ne$', word)
        if matches:
            return matches.group(1)

class DisambiguatorBaliSuffixRule19c(object):
    def disambiguate(self, word):
        #print(word)
        matches = re.match(r'^(.*[aiueobcdfghjklmnpqrstvwxyz])nne$', word)
        if matches:
            return matches.group(1)


