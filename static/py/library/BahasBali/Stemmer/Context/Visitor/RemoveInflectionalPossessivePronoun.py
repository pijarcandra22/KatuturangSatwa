import re
from static.py.library.BahasBali.Stemmer.Context.Removal import Removal

class RemoveInflectionalPossessivePronoun(object):
    def visit(self, context):
        result = self.remove(context.current_word)
        if result != context.current_word:
            removedPart = re.sub(result, '', context.current_word, 1)

            removal = Removal(self, context.current_word, result, removedPart, 'PP')

            context.add_removal(removal)
            context.current_word = result

    def remove(self, word):
        #matches = re.match(r'^(.*[e])$', word)
        return re.sub(r'(e|ne|nne)$', '', word, 1)

