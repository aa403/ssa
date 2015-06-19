#!/usr/bin/python
import json

class SentimentAnalysis(object):

    def __init__(self, sentiment_score, decision):
        self.sentiment_score = sentiment_score
        self.decision = decision

    def to_dict(self):
        dictionary_representation = {
            'sentiment_scores': self.sentiment_score.to_dict(),
            'decision': self.decision
        }
        return dictionary_representation

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return str(self.sentiment_score) + ';' + str(self.decision)

class SentimentScore(object):

    def __init__(self, positive, negative, subjectivity):
        self.positive = positive
        self.negative = negative
        self.neutral = positive - negative
        self.subjectivity = subjectivity

    def __str__(self):
        return str(self.positive) + ";" + str(self.negative) + ";" + str(self.neutral) + ";" + str(self.subjectivity)

    def to_dict(self):
        dict_representation = {
            'positive': self.positive,
            'negative': self.negative,
            'neutral': self.neutral,
            'subjectivity': self.subjectivity
        }
        return dict_representation

    def __repr__(self):
        return str(self.to_dict())

    def to_json(self):
        return json.dumps(self.to_dict())

    def add_value(self, positive, negative, subjectivity):
        self.positive += positive
        self.negative += negative
        self.subjectivity += subjectivity

class SentimentWord(object):
    def __init__(self, pos, id_number, positive_score, negative_score, syn_terms, gloss):
        self.pos = pos
        self.id_number = id_number
        self.positive_score = positive_score
        self.negative_score = negative_score
        self.syn_terms = syn_terms
        self.gloss = gloss

    def __str__(self):
        return self.pos + ',' + str(self.id_number) + ',' + str(self.positive_score) + ',' + str(self.negative_score) + ',' + self.syn_terms + ',' + self.gloss

    def __repr__(self):
        return self.pos + ',' + str(self.id_number) + ',' + str(self.positive_score) + ',' + str(self.negative_score) + ',' + self.syn_terms + ',' + self.gloss



class Sentence(object):
    def __init__(self, sentence, tagged, tokens, tagged_tokens, lemmas):
        self.sentence = sentence
        self.tagged = tagged
        self.tokens = tokens
        self.tagged_tokens = tagged_tokens
        self.lemmas = lemmas

    def __str__(self):
        return self.sentence + '\t' + self.tagged + '\t' + str(self.tokens) + '\t' + str(self.tagged_tokens) + '\t' + str(self.lemmas)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        dict_representation = {
            'sentence': self.sentence,
            'tagged': self.tagged
            # ,
            # 'tokens': str(self.tokens,
            # 'tagged_tokens': str(self.tagged_tokens,
            # 'lemmas': str(self.lemmas)
        }
        return dict_representation
