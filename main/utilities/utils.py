__author__ = 'sslr'

from copy import deepcopy

from src.main.utilities import enums

def matches_pos(sentiment_pos, pos_tag):
    tag_list = enums.TAG_SET.get(sentiment_pos)

    for tag in tag_list:
        if tag == pos_tag:
            return True

    return False


def is_relevant_word(pos_tag):

    #relevant_words = deepcopy(enums.TAG_SET.get("n"))
    relevant_words = deepcopy(enums.TAG_SET.get("a"))
    # relevant_words.extend(enums.TAG_SET.get("r"))
    # relevant_words.extend(enums.TAG_SET.get("n"))
    relevant_words.extend(enums.TAG_SET.get("v"))

    for tag in relevant_words:
        if tag == pos_tag:
            return True

    return False




