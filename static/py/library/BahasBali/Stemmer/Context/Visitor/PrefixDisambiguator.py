from static.py.library.BahasBali.Stemmer.Context.Visitor.AbstractDisambiguatePrefixRule import AbstractDisambiguatePrefixRule

class PrefixDisambiguator(AbstractDisambiguatePrefixRule):
    """description of class"""

    def __init__(self, disambiguators):
        #print(disambiguators)
        #print('a')
        super(PrefixDisambiguator, self).__init__()

        self.add_disambiguators(disambiguators)



