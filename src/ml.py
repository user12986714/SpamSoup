# coding=utf-8

import re

import msg
from stopword import stopword


ml_config = None


def config(cfg):
    """ Write ml_config. """
    global ml_config
    ml_config = cfg


def tokenize_string(string):
    """ Split a string into tokens. """
    # Argument: string
    # Returns: a list of tokens

    tokens = re.compile(r"[-\w']+").findall(string.lower())
    return [tokens[i] for i in range(len(tokens)) if tokens[i] not in stopword]


def naive_tokenizer(post_tuple):
    """ Naive tokenizer, splitting string at non-word chars and remove stopwords. """
    # Argument: the tuple returned by get_post() or ms_ws_listener()
    # Returns: tokenized string list

    unified_user_site_id = "##USR## " + post_tuple[2][1] + " ::@:: " + post_tuple[2][0]
    tokenized_post = list()

    tokenized_post.append(unified_user_site_id)
    tokenized_post.append(post_tuple[2][2])  # This is the username
    tokenized_post.extend(tokenize_string(post_tuple[0]))
    tokenized_post.extend(tokenize_string(post_tuple[1]))

    return [x for x in tokenized_post if x]


def feedback_over_threshold(post_id, feedbacks):
    """ Determine if feedbacks for a post is over learning threshold. """
    # Note: post_id can be anything printable with .format()
    # It is only used for outputting and not related to core functionalities.

    tp_count = 0
    fp_count = 0
    naa_count = 0

    for user, feedback in feedbacks:
        if feedback.startswith("tp"):
            tp_count += 1
            continue

        if feedback.startswith("fp"):
            fp_count += 1
            continue

        if feedback.startswith("naa") or feedback.startswith("ignore"):
            naa_count += 1
            continue

        msg.output("Feedback {} by {} on post {} not recognized.".format(feedback, user, post_id), msg.DEBUG, tags=["Feedback"])

    msg.output("Feedback for post {} extracted as {}/{}/{}.".format(post_id, tp_count, fp_count, naa_count), msg.VERBOSE, tags=["Feedback"])

    w_tp = tp_count + ml_config["feedback"]["naa_to_tp"] * naa_count
    w_fp = fp_count + ml_config["feedback"]["naa_to_fp"] * naa_count
    msg.output("Weighed feedback for post {} calculated as {}/{}.".format(post_id, w_tp, w_fp), msg.VERBOSE, tags=["Feedback"])

    if w_fp == 0 and w_tp >= ml_config["feedback"]["un_thres"]:
        return True
    if w_tp == 0 and w_fp >= ml_config["feedback"]["un_thres"]:
        return False

    if w_tp and w_fp:
        if w_tp / w_fp >= ml_config["feedback"]["co_thres"]:
            return True
        if w_fp / w_tp >= ml_config["feedback"]["co_thres"]:
            return False

    # Not over threshold yet
    return None


def analyze_post(post_id, post_tuple):
    """ Call appropriate executables to analyze the post. """
    pass


def learn_post(post_id, post_tuple, is_tp):
    """ Call appropriate executables to learn the post. """
    pass
