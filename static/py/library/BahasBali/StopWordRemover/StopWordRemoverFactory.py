from static.py.library.BahasBali.Dictionary.ArrayDictionary import ArrayDictionary
from static.py.library.BahasBali.StopWordRemover.StopWordRemover import StopWordRemover

class StopWordRemoverFactory(object):
    """description of class"""

    def create_stop_word_remover(self):
        stopWords = self.get_stop_words()

        dictionary = ArrayDictionary(stopWords)
        stopWordRemover = StopWordRemover(dictionary)
        #print(stopWordRemover)
        return stopWordRemover

    def get_stop_words(self):
        return ['i','ia','anggen', 'lan','sane','ring','miwah','puniki','olih','lantas','di','ka',\
                'suba','pan','ida','buin','tur','ada','sang','teken','anak','teken','jani','keto',\
                'titiang','luh','cai','ja','ento','pada','mara','ditu','ne','kone','tiang',\
                'tusing','bapa','ajak','ane','adi','tusing','dadi','aji','n','g','t','ipun','tan','kadi',\
                'san','sampun','med','ih']




