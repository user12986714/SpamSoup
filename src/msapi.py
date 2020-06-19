# coding=utf-8

import requests
import dataproc


ms_config = None


def config(cfg):
    """ Write ms_config. """
    global ms_config
    ms_config = cfg


def get_feedback(post_id):
    """ Get the list of feedback on post. """
    # Returns: [(uid, feedback)]
    global ms_config

    route = '{}/api/v2.0/feedbacks/post/' +\
            '{}?key={}&filter=JJLFGJOFIOMFLGHJLHNIFMGJILKJKHOLMHIFGGOLFNIHF'
    response = requests.get(route.format(ms_config["ms_host"], post_id, ms_config["api_key"]))

    try:
        data = response.json()
        feedbacks = list()
        for item in data["items"]:
            feedback = (item["user_name"], item["feedback_type"])
            feedbacks.append(feedback)

        return feedbacks
    except Exception:
        raise ValueError("Getting post {} failed: Invalid response.".format(post_id))


def get_post(post_id):
    """ Get the post. """
    # Returns: (post_title, post_body, user_tuple)
    global ms_config

    route = '{}/api/v2.0/posts/' +\
            '{}?key={}&filter=MLLKIHJMHIHKKFMJLLHGMKIMMGOKFFN'
    response = requests.get(route.format(ms_config["ms_host"], post_id, ms_config["api_key"]))

    try:
        data = response.json()
        user = dataproc.get_user(data["items"][0]["user_link"], data["items"][0]["username"])
        return (data["items"][0]["title"], data["items"][0]["body"], user)
    except Exception:
        raise ValueError("Getting feedback for post {} failed: Invalid response.".format(post_id))
