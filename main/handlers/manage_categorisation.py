__author__ = 'sslr'

import src.main.algorithms.categorisation as algorithm

def run_categorisation(filename):
    # filename = "../docs/MMCustomerTesting2015-FeedbackandActions-small.csv"
    # filename = "../docs/raw-comments-first-question.txt"
    categories = algorithm.find_category(filename)
    print '\n\nSentiment score for comments in file ' + filename

    for category in categories.keys():
        score = categories.get(category)

        print "\"" + category + "\"\n\t" + str(score)

        if score.positive > score.negative:
            print "\tsentiment score is POSITIVE (" + str(score.positive) + ")"
        elif score.negative > score.positive:
            print "\tsentiment score is NEGATIVE (" + str(score.negative) + ")"
        elif score.subjectivity == 0:
            print "\tsentiment score is NEUTRAL (" + str(score.subjectivity) + ")"
        else:
            print "\tno sentiment score was found"
