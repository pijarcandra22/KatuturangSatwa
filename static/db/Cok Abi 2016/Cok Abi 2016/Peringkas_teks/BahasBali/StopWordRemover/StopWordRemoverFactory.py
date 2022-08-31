from BahasBali.Dictionary.ArrayDictionary import ArrayDictionary
from BahasBali.StopWordRemover.StopWordRemover import StopWordRemover

class StopWordRemoverFactory(object):
    """description of class"""

    def create_stop_word_remover(self):
        stopWords = self.get_stop_words()

        dictionary = ArrayDictionary(stopWords)
        stopWordRemover = StopWordRemover(dictionary)
        print(stopWordRemover)
        return stopWordRemover

    def get_stop_words(self):
        return ['anggen', 'lan','sane','ring','miwah','puniki','olih']




