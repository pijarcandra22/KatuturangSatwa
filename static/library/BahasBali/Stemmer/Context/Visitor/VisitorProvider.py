from BahasBali.Stemmer.Context.Visitor.DontStemShortWord import DontStemShortWord
from BahasBali.Stemmer.Context.Visitor.RemoveInflectionalParticle import RemoveInflectionalParticle
# from BahasBali.Stemmer.Context.Visitor.RemoveSuffix1 import RemoveSuffix1
# from BahasBali.Stemmer.Context.Visitor.RemoveSuffix2 import RemoveSuffix2
# from BahasBali.Stemmer.Context.Visitor.RemoveSuffix3 import RemoveSuffix3
# from BahasBali.Stemmer.Context.Visitor.RemoveSuffix4 import RemoveSuffix4
from BahasBali.Stemmer.Context.Visitor.RemoveDerivationalSuffix import RemoveDerivationalSuffix
from BahasBali.Stemmer.Context.Visitor.RemoveInflectionalPossessivePronoun import RemoveInflectionalPossessivePronoun
from BahasBali.Stemmer.Context.Visitor.PrefixDisambiguator import PrefixDisambiguator
from BahasBali.Stemmer.Context.Visitor.SuffixDisambiguator import SuffixDisambiguator
from BahasBali.Stemmer.Context.Visitor.RemovePlainPrefix import RemovePlainPrefix

from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule1 import DisambiguatorBaliPrefixRule1a, DisambiguatorBaliPrefixRule1b,DisambiguatorBaliPrefixRule1c, DisambiguatorBaliPrefixRule1d, DisambiguatorBaliPrefixRule1e
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule2 import DisambiguatorBaliPrefixRule2a, DisambiguatorBaliPrefixRule2b,DisambiguatorBaliPrefixRule2c
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule3 import DisambiguatorBaliPrefixRule3a, DisambiguatorBaliPrefixRule3b
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule4 import DisambiguatorBaliPrefixRule4a, DisambiguatorBaliPrefixRule4b,DisambiguatorBaliPrefixRule4c,DisambiguatorBaliPrefixRule4d,DisambiguatorBaliPrefixRule4e,DisambiguatorBaliPrefixRule4f,DisambiguatorBaliPrefixRule4g
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule6 import DisambiguatorBaliPrefixRule6a, DisambiguatorBaliPrefixRule6b, DisambiguatorBaliPrefixRule6c
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule7 import DisambiguatorBaliPrefixRule7a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule8 import DisambiguatorBaliPrefixRule8a, DisambiguatorBaliPrefixRule8b, DisambiguatorBaliPrefixRule8c, DisambiguatorBaliPrefixRule8d, DisambiguatorBaliPrefixRule8e, DisambiguatorBaliPrefixRule8f, DisambiguatorBaliPrefixRule8g
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule9 import DisambiguatorBaliPrefixRule9a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule10 import DisambiguatorBaliPrefixRule10a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliPrefixRule11 import DisambiguatorBaliPrefixRule11a
#==============SESELAN======================
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSeselanRule12 import DisambiguatorBaliSeselanRule12a, DisambiguatorBaliSeselanRule12b
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSeselanRule13 import DisambiguatorBaliSeselanRule13a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSeselanRule14 import DisambiguatorBaliSeselanRule14a, DisambiguatorBaliSeselanRule14b
#==================WEWEHAN======================
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliWewehanRule15 import DisambiguatorBaliWewehanRule15a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliWewehanRule16 import DisambiguatorBaliWewehanRule16a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliWewehanRule17 import DisambiguatorBaliWewehanRule17a
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliWewehanRule18 import DisambiguatorBaliWewehanRule18a
#=================PENGIRING================
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSuffixRule19 import DisambiguatorBaliSuffixRule19a, DisambiguatorBaliSuffixRule19b, DisambiguatorBaliSuffixRule19c
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSuffixRule20 import DisambiguatorBaliSuffixRule20a, DisambiguatorBaliSuffixRule20b, DisambiguatorBaliSuffixRule20c, DisambiguatorBaliSuffixRule20d,DisambiguatorBaliSuffixRule20e
from BahasBali.Morphology.Disambiguator.DisambiguatorBaliSuffixRule21 import DisambiguatorBaliSuffixRule21a, DisambiguatorBaliSuffixRule21b, DisambiguatorBaliSuffixRule21c, DisambiguatorBaliSuffixRule21d


class VisitorProvider(object):
    """description of class"""

    def __init__(self):
        self.visitors = []
        self.suffix_visitors = []
        self.prefix_pisitors = []

        self.init_visitors()

    def init_visitors(self):
        self.visitors.append(DontStemShortWord())

        self.suffix_visitors.append(SuffixDisambiguator(\
            [DisambiguatorBaliSuffixRule19a(), DisambiguatorBaliSuffixRule19b(), DisambiguatorBaliSuffixRule19c()]))
        self.suffix_visitors.append(SuffixDisambiguator( \
            [DisambiguatorBaliSuffixRule20a(), DisambiguatorBaliSuffixRule20b(), DisambiguatorBaliSuffixRule20c(), DisambiguatorBaliSuffixRule20d(), DisambiguatorBaliSuffixRule20e()]))
        self.suffix_visitors.append(SuffixDisambiguator( \
            [DisambiguatorBaliSuffixRule21a(), DisambiguatorBaliSuffixRule21b(), DisambiguatorBaliSuffixRule21c(), DisambiguatorBaliSuffixRule21d()]))

        #{lah|kah|tah|pun}
        self.suffix_visitors.append(RemoveInflectionalParticle())
        # #{ku|mu|nya}
        self.suffix_visitors.append(RemoveInflectionalPossessivePronoun())
        # #{i|kan|an}
        self.suffix_visitors.append(RemoveDerivationalSuffix())

        #self.suffix_visitors.append(RemoveSuffix())

        #{di|ka|ke}
        self.prefix_pisitors.append(RemovePlainPrefix())

        disambiguators1 = [DisambiguatorBaliPrefixRule1a(), DisambiguatorBaliPrefixRule1b(), \
            DisambiguatorBaliPrefixRule1c(), DisambiguatorBaliPrefixRule1d(), DisambiguatorBaliPrefixRule1e()]
        self.prefix_pisitors.append(PrefixDisambiguator(disambiguators1))
        disambiguators2 = [DisambiguatorBaliPrefixRule2a(), DisambiguatorBaliPrefixRule2b(), \
            DisambiguatorBaliPrefixRule2c()]
        self.prefix_pisitors.append(PrefixDisambiguator(disambiguators2))
        disambiguators3 = [DisambiguatorBaliPrefixRule3a(), DisambiguatorBaliPrefixRule3b()]
        self.prefix_pisitors.append(PrefixDisambiguator(disambiguators3))
        disambiguators4 = [DisambiguatorBaliPrefixRule4a(), DisambiguatorBaliPrefixRule4b(), \
            DisambiguatorBaliPrefixRule4c(),DisambiguatorBaliPrefixRule4d(),DisambiguatorBaliPrefixRule4e(),DisambiguatorBaliPrefixRule4f(),DisambiguatorBaliPrefixRule4g()]
        self.prefix_pisitors.append(PrefixDisambiguator(disambiguators4))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliPrefixRule6a(),DisambiguatorBaliPrefixRule6b(),DisambiguatorBaliPrefixRule6c()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliPrefixRule7a()]))
        disambiguators8 = [DisambiguatorBaliPrefixRule8a(), DisambiguatorBaliPrefixRule8b(), \
                           DisambiguatorBaliPrefixRule8c(), DisambiguatorBaliPrefixRule8d(), \
                           DisambiguatorBaliPrefixRule8e(), DisambiguatorBaliPrefixRule8f(), \
                           DisambiguatorBaliPrefixRule8g()]
        self.prefix_pisitors.append(PrefixDisambiguator(disambiguators8))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliPrefixRule9a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliPrefixRule10a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliPrefixRule11a()]))
        #===============================SESELAN==========================================
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliSeselanRule12a(), DisambiguatorBaliSeselanRule12b()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliSeselanRule13a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliSeselanRule14a(), DisambiguatorBaliSeselanRule14b()]))
        #===============================WEWEHAN========================================
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliWewehanRule15a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliWewehanRule16a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliWewehanRule17a()]))
        self.prefix_pisitors.append(PrefixDisambiguator([DisambiguatorBaliWewehanRule18a()]))


    def get_visitors(self):
        return self.visitors

    def get_suffix_visitors(self):
        return self.suffix_visitors

    def get_prefix_visitors(self):
        return self.prefix_pisitors

