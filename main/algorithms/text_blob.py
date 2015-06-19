__author__ = 'sslr'


from textblob import TextBlob

from src.main.nlp_core.models import SentimentScore

def find_sentiment(comment_list):

    sentiment_scores = dict()

    print "Computing sentiment scores..."
    # 1.
    for comment in comment_list.keys():
        sentence = comment_list.get(comment)

        sentiment = TextBlob(sentence.sentence).sentiment
        positive = sentiment.polarity if sentiment.polarity > 0 else 0
        negative = sentiment.polarity if sentiment.polarity < 0 else 0
        sentiment_scores[comment] = SentimentScore(positive, negative, sentiment.subjectivity)

    return sentiment_scores
