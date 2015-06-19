__author__ = 'sslr'

import re
import csv

from src.main.nlp_core.models import SentimentWord


class Inquirer:
    filename = "../docs/inquirerbasic.csv"
    global senti_wordnet

    def __init__(self):
        self.senti_wordnet = dict()
        self.read_file()

    def read_file(self):

        id = 1
        with open(self.filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                key = re.sub(r"^(.+)(#\d+)$", r"\1", row[0].lower())
                word_info = SentimentWord(key, id, 1 if row[1] == 'Positiv' else 0, 1 if row[2] == 'Negativ' else 0,
                                          key, row[4])

                self.senti_wordnet.setdefault(key, [])
                self.senti_wordnet[key].append(word_info)
                id += 1