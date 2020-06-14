#!/usr/bin/env python3
# coding=utf-8

""" Config for metasmoke and tokenizers. """


class Config:
    """ Configurations for glueware and MS interface. """
    # Metasmoke interface
    ms_key = "your_ms_key_here"
    ms_host = "ms_host_here"
    ms_ws_host = "ms_websocket_host_here"
    ms_ws_max_retries = 5  # Max retries before giving up

    # Feedback threshold
    naa_bias = 0.5  # Need to be in [0, 1]
    un_thres = 2  # Threshold for unanimous feedbacks
    co_thres = 3  # Ratio threshold for controversial feedbacks

    # Binary location
    # Vectorizing
    sbph_bin_loc = "/abs/path/to/sbph"
    ngram_bin_loc = "/abs/path/to/ngram"
    bow_bin_loc = "/abs/path/to/bow"
    # Classifying
    nbc_bin_loc = "/abs/path/to/nbc"

    # Data file
    sbph_nbc_dat_loc = "/abs/path/to/sbph/nbc/data"
    ngram_nbc_dat_loc = "/abs/path/to/ngram/nbc/data"
    bow_nbc_dat_loc = "/abs/path/to/bow/nbc/data"


class Location:
    """ Configurations for location. """
    admin = "me"  # The user running this instance
    name = "my_instance"  # The name for this instance


class Version:
    """ Version information. """
    # Please don't change any value in this class when configuring.
    major = 0
    alias = "Unsure"
    minor = 0
