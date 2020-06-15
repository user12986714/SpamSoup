#!/usr/bin/env python3
# coding=utf-8

""" Implements naive tokenizer, generating word tokens and remove stopwords. """
stopword = ["stopword list here"]


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
