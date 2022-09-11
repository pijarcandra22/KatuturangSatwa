from static.py.library.BahasBali.Stemmer.Context.Visitor.AbstractDisambiguateSuffixRule import AbstractDisambiguateSuffixRule

class SuffixDisambiguator(AbstractDisambiguateSuffixRule):
    """description of class"""

    def __init__(self, disambiguators):
        super(SuffixDisambiguator, self).__init__()

        self.add_disambiguators(disambiguators)



