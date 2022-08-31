import re
from BahasBali.Stemmer.Context.Removal import Removal

class RemovePlainPrefix(object):

    def visit(self, context):
        result = self.remove(context.current_word)
        if result != context.current_word:
            removedPart = re.sub(result, '', context.current_word, 1)

            removal = Removal(self, context.current_word, result, removedPart, 'DP')

            context.add_removal(removal)
            context.current_word = result

    def remove(self, word):
        #print('a')
        """Remove plain prefix : di|ka|ke"""
        return re.sub(r'^(di|ka|ke)', '', word, 1)








