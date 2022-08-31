import re
from BahasBali.Stemmer.Context.Removal import Removal

class RemoveDerivationalSuffix(object):
    def visit(self, context):
        result = self.remove(context.current_word)
        if result != context.current_word:
            removedPart = re.sub(result, '', context.current_word, 1)

            removal = Removal(self, context.current_word, result, removedPart, 'DS')

            context.add_removal(removal)
            context.current_word = result

    def remove(self, word):
        return re.sub(r'(ang|nang|yang|na|nan|a|ana)$', '', word, 1)


