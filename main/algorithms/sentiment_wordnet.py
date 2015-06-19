__author__ = 'sslr'

import re

from src.main.nlp_core.models import SentimentWord
from src.main.nlp_core.models import SentimentScore
from src.main.utilities import utils


class SentimentWordnet(object):
    filename = "../docs/SentiWordNet_3.0.0_20130122.txt"
    senti_wordnet = dict()

    def __init__(self):
        self.read_file()

    def read_file(self):

        current_file = open(self.filename, "r")
        file_text = current_file.read()

        split = file_text.split('\n')

        for string in split:

            if not string.startswith("#") and string.count("\t") >= 4:
                items = string.split("\t")
                terms = items[4].split(" ")
                word_info = SentimentWord(items[0], int(items[1]), float(items[2]), float(items[3]), items[4], items[5])
                for term in terms:
                    key = re.sub(r"^(.+)(#\d+)$", r"\1", term.lower())
                    self.senti_wordnet.setdefault(key, [])
                    self.senti_wordnet[key].append(word_info)

    def get_sentiment_score(self, lemma, token, tagged_token):
        """
        :rtype : SentimentScore
        """
        wordnet_key = lemma

        if not self.senti_wordnet.__contains__(wordnet_key):
            wordnet_key = token

        wordnet_words = self.senti_wordnet.get(wordnet_key.lower())
        sentiment_score = SentimentScore(0, 0, 0)

        negativity = 0
        positivity = 0

        if wordnet_words is not None:

            for wordnet_word in wordnet_words:

                if utils.matches_pos(wordnet_word.pos, tagged_token):
                    negativity += wordnet_word.negative_score
                    positivity += wordnet_word.positive_score

            sentiment_score = SentimentScore(positivity / len(wordnet_words), negativity / len(wordnet_words), 0)

        return sentiment_score

    def find_sentiment_score(self, comment_list):

        """
        Parameters:
        comment_list :  dict(key: String, value: Sentence)
        -----
        :rtype: dict(key: String, value: SentimentScore)
        """

        senti_score = dict()

        print "Computing sentiment scores..."
        # 1. takes each comment tagged version
        # 2. looks for all its words in wordnet
        # 3. averages their positive and negative sentiment values
        # 4. provides a sentiment score for each comment computed as:

        for comment in comment_list.keys():

            sentence = comment_list.get(comment)
            total_positive = 0
            total_negative = 0
            words_added = []

            # iterate over the tokens of the comment
            for i in range(len(sentence.tokens)):

                # Checks if the token is a relevant word to take into account.
                # If it is stores both its negative and positive values (at this point we are using adjectives
                # and verbs as relevant words.
                if utils.is_relevant_word(sentence.tagged_tokens[i]):

                    current_sc = self.get_sentiment_score(sentence.lemmas[i], sentence.tokens[i],
                                                          sentence.tagged_tokens[i])
                    total_positive += current_sc.positive
                    total_negative += current_sc.negative
                    words_added.append(sentence.lemmas[i] + "/" + sentence.tagged_tokens[i] + "/" + str(current_sc))

                elif sentence.lemmas[i] == 'not' or sentence.lemmas[i] == 'no':

                    # if this token is a "not/no", we take into account its negative value twice and we also get only
                    # the negative values of the two words that follow it, ignoring the positive value.
                    current_sc = self.get_sentiment_score(sentence.lemmas[i], sentence.tokens[i],
                                                          sentence.tagged_tokens[i])
                    total_negative += current_sc.negative
                    words_added.append(sentence.lemmas[i] + "/" + sentence.tagged_tokens[i] + "/" + str(current_sc))

                    j = i + 1
                    if j < len(sentence.lemmas):

                        if not sentence.lemmas[j] in words_added:
                            prev_sc = self.get_sentiment_score(sentence.lemmas[j], sentence.tokens[j],
                                                               sentence.tagged_tokens[j])
                            total_negative += prev_sc.negative
                            words_added.append(sentence.lemmas[j])

                    j = i + 2
                    if j < len(sentence.lemmas):

                        if not sentence.lemmas[j] in words_added:
                            prev_sc = self.get_sentiment_score(sentence.lemmas[j], sentence.tokens[j],
                                                               sentence.tagged_tokens[j])
                            total_negative += prev_sc.negative
                            words_added.append(sentence.lemmas[j])

            # Stores the total value of the positive and negative values found for the tokens of this sentence and divides
            # them by the number of words taken into account when computing the total values.
            total_words = len(words_added) if len(words_added) > 0 else 1
            senti_score[comment] = SentimentScore(total_positive / total_words,
                                                  total_negative / total_words, 0)

        return senti_score
