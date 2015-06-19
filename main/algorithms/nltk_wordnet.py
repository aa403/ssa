#!/usr/bin/python

from nltk.corpus import wordnet as wn

class Wordnet(object):

    @staticmethod
    def synsets(word):
        return wn.synsets(word)

    @staticmethod
    def hypernyms(word):
        return wn.hypernyms(word)

    @staticmethod
    def get_common_hypernym(synsets1, synsets2):
        for synset1 in synsets1:
            for synset2 in synsets2:
                current_common_hypernym = synset1.lowest_common_hypernyms(synset2)
                if current_common_hypernym is not None:
                    return current_common_hypernym

        return None

    @staticmethod
    def are_connected(word1, word2):
        synsets1 = wn.synsets(word1)
        synsets2 = wn.synsets(word2)
        return self.get_common_hypernym(synsets1, synsets2)

