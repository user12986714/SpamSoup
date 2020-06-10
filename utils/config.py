#!/usr/bin/env python3
# coding=utf-8

""" Config for metasmoke and tokenizers. """


class Config:
    """ Config here. """
    ms_key = "your_ms_key_here"
    ms_host = "ms_host_here"
    ms_ws_host = "ms_websocket_host_here"
    MS_WS_MAX_RETRIES = 5  # Max retries before giving up

    naa_bias = 0.5  # Change to whatever you like as long as 0 <= naa_bias <= 1
    un_thres = 2  # Threshold for unanimous feedbacks
    co_thres = 3  # Ratio threshold for controversial feedbacks
