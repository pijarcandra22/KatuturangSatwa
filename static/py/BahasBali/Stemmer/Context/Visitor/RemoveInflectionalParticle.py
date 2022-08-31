import re
from BahasBali.Stemmer.Context.Removal import Removal

class RemoveInflectionalParticle(object):
    def visit(self, context):
        #print(context.current_word)
        result = self.remove(context.current_word)
        #print(result)
        if result != context.current_word:
            removedPart = re.sub(result, '', context.current_word, 1)
            #print(removedPart)
            
            removal = Removal(self, context.current_word, result, removedPart, 'P')
            #print(removal)

            context.add_removal(removal)
            #print(context)
            context.current_word = result
            #print(context.current_word)

    def remove(self, word):
        #print(word)
        #print(re.sub(r'-*(lah|kah|tah|pun)$', word))
        return re.sub(r'(ing|ning|n|in|nin|ina)$', '', word, 1)



