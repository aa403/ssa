__author__ = 'sslr'

from src.main.nlp_core.models import SentimentScore
from src.main.nlp_core.models import SentimentAnalysis
from src.main.nlp_core.annotation import Annotator
from src.main.algorithms.sentiment_wordnet import SentimentWordnet

def manage_sentiment_analysis(annotator, wordnet, comments):
    """
    :rtype : SentimentAnalysis
    """
    if annotator:
        annotated_comments = annotator.annotate_list(comments)
    else:
        annotated_comments = comments

    my_sentiment = wordnet.find_sentiment_score(annotated_comments)
    combined_values = combine_values(my_sentiment)

    sentiment_analysis = draw_decision(combined_values)

    return sentiment_analysis

def draw_decision(combined_values):
    """
    :rtype : SentimentAnalysis
    """
    decision_dict = dict()

    for key, value in combined_values.iteritems():
        if value.positive - value.negative > 0:
            decision = 'POSITIVE'
        elif value.positive - value.negative < 0:
            decision = 'NEGATIVE'
        else:
            decision = 'NEUTRAL'

        decision_dict[key] = SentimentAnalysis(value, decision)

    return decision_dict


def combine_values(*sentiment_values):

    final_score = dict()

    for sentiment_value in sentiment_values:

        for comment in sentiment_value.keys():
            current_score_value = sentiment_value.get(comment)
            final_score_value = final_score.get(comment)

            if not final_score_value:
                final_score_value = current_score_value
            else:
                subjectivity = final_score_value.subjectivity + current_score_value.subjectivity
                positive = ((final_score_value.positive + current_score_value.positive) / 2) - subjectivity
                negative = ((final_score_value.negative + current_score_value.negative) / 2) - subjectivity
                final_score_value = SentimentScore(positive, negative, subjectivity)

            final_score[comment] = final_score_value

    return final_score

if __name__ == "__main__":
    # run_sentiment()
    # filename = "../docs/raw-comments-first-question.txt"
    # filename = "../docs/clean.txt"
    # filename = "../docs/raw-comments-spender-useful.txt"
    # filename = "../docs/raw-comments-spender-design.txt"
    filename = "../docs/raw-comments-spender-enjoyed.txt"
    sentiment_wordnet = SentimentWordnet()
    comments = Annotator().annotate_file(filename)
    final_analysis = manage_sentiment_analysis(None, sentiment_wordnet, comments)
    print str(final_analysis)

