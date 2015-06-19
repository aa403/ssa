__author__ = 'sslr'
from src.main.nlp_core.annotation import Annotator
from src.main.algorithms.sentiment_wordnet import SentimentWordnet
from src.main.handlers.manage_sentiment import manage_sentiment_analysis

class SentimentAnalysis(object):

    def __init__(self):
        self.wordnet = SentimentWordnet()
        self.annotator = Annotator()

    def analyse_sentiment(self, comments):
        """
        Analyses the sentiment for the given list of strings.
        :rtype : dict which keys are the comments and the values are the sentiment predicted values
        { <comment[i]> : {
            'sentiment_scores': {
                'positive': X,
                'negative': Y,
                'neutral': Z,
                'subjectivity': 0
            },
            'decision': <decision value>
            }
            ...
        }
        """
        return manage_sentiment_analysis(self.annotator, self.wordnet, comments)
