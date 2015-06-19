__author__ = 'sslr'
#!/usr/bin/statistical_sentiment_analysis


import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import nltk.data
import nltk.tag
import csv

from src.main.nlp_core.models import Sentence

class Annotator(object):

    def __init__(self):
        self.tagger = nltk.data.load(nltk.tag._POS_TAGGER)
        self.lemmatizer = WordNetLemmatizer()

    def annotate(self, text):
        """
        Parameter:
        text: String
        ----
        :rtype : Sentence
        """
        tokens = nltk.word_tokenize(text)
        tagged = self.tagger.tag(tokens)
        final_annotation = ""
        lemmas = []
        tagged_tokens = []

        for i in xrange(len(tokens)):
            lemma = self.lemmatizer.lemmatize(tokens[i])
            tagged_token = tagged[i][1]
            final_annotation += tokens[i] + "/" + tagged_token + "/" + lemma + " "
            tagged_tokens.append(tagged_token)
            lemmas.append(lemma)

        return Sentence(text, final_annotation, tokens, tagged_tokens, lemmas)

    def annotate_list(self, comments):
        """
        Parameter:
        comment: list(String)
        ----
        :rtype : dict(key:String, value:Sentence)
        """

        text_list = dict()

        for string in comments:

            comment = string.replace("^\'", "")
            comment = comment.replace("\'$", "")
            comment = comment.replace("^\"", "")
            comment = comment.replace("\"$", "").strip()

            if comment:
                text_list[comment] = self.annotate(comment)

        return text_list

    def annotate_file(self, filename):
        """
        Parameter:
        filename: String
        ----
        :rtype : dict(key:String, value:Sentence)
        """
        print "Annotating input file: " + filename
        text_list = dict()
        current_file = open(filename, "r")
        file_text = current_file.read()

        split = file_text.split("\n")

        for string in split:
            comment = string.replace("\'", "")
            comment = comment.replace("\"", "").strip()

            if comment:
                text_list[comment] = self.annotate(comment)

        return text_list

    def annotate_spreadsheet(self, filename):

        text_list = dict()
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')
            for row in spamreader:
                comment = row[2].replace("\'", "")
                comment = comment.replace("\"", "")
                text_list[comment] = self.annotate(comment)

        return text_list
