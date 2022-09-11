import re
from static.py.library.BahasBali.Stemmer.Context.Removal import Removal

class RemoveSuffix1(object):

    def visit(self, context):
        result = self.remove(context.current_word)
        if result != context.current_word:
            removedPart = re.sub(result, '', context.current_word, 1)

            removal = Removal(self, context.current_word, result, removedPart, 'DS')

            context.add_removal(removal)
            context.current_word = result

    def remove(self, word):
        #print(word)
        #return re.sub(r'(ang|nang|yang|an|nan|a|na|n|e|ing|ning|e|ne|nne|in)$', '', word, 1)

        return re.sub(r'(a|n|e)$', '', word, 1)


