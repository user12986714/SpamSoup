#!/usr/bin/env python3
# coding=utf-8

""" Communicates with ms and calls appropriate executables. """
import re
import json
import subprocess
import requests
import websocket
from config import Config


def get_feedback_on_post(post_id):
    """ Get the list of feedback on post. """
    # Returns: A list of tuples with each in format (uid, feedback).

    route = 'https://metasmoke.erwaysoftware.com/api/v2.0/feedbacks/post/' +\
            '{}?key={}&filter=JJLFGJOFIOMFLGHJLHNIFMGJILKJKHOLMHIFGGOLFNIHF'
    response = requests.get(route.format(post_id, Config.ms_key))
    data = response.json()

    feedbacks = list()
    for item in data["items"]:
        feedback = (item["user_name"], item["feedback_type"])
        feedbacks.append(feedback)

    return feedbacks


def get_post(post_id):
    """ Get the post. """
    # Returns: A tuple (post_title, post_body, (user_site, user_id, user_name))

    route = 'https://metasmoke.erwaysoftware.com/api/v2.0/posts/' +\
            '{}?key={}&filter=MLLKIHJMHIHKKFMJLLHGMKIMMGOKFFN'
    response = requests.get(route.format(post_id, Config.ms_key))
    data = response.json()

    user_link = data["items"][0]["user_link"]
    user_re = re.search(r'^https?:\/\/([a-z.]+)\/users\/([0-9]+)', user_link)

    user = (user_re.group(0), user_re.group(1),
            data["items"][0]["username"])

    return (data["items"][0]["title"], data["items"][0]["body"], user)


def conn_ms_ws():
    """ Connect to metasmoke websocket. """
    try:
        ws = websocket.create_connection(Config.ms_ws_host, origin=Config.ms_host)
        idf = r'{"channel": "ApiChannel",' +\
              r'"key": "{}",'.format(Config.ms_key) +\
              r'"events": "feedbacks#update;posts#create"}'
        payload = json.dumps({"command": "subscribe", "identifier": idf})
        ws.send(payload)
        ws.settimeout(10)
        return ws
    except Exception:
        return None


def init_ms_ws():
    """ Initiate metasmoke websocket. """
    failure_count = 0
    while failure_count < Config.MS_WS_MAX_RETRIES:
        ws = conn_ms_ws()
        if ws:
            return ws

    # Give up
    raise RuntimeError("Cannot connect to MS websocket.")


def ms_ws_listener():
    """ Metasmoke websocket listener. """
    ws = init_ms_ws()
    while True:
        try:
            resp = ws.recv()
            data = json.loads(resp)

            if "type" in data:
                if data["type"] == "reject_subscription":
                    raise RuntimeError("MS WS connection rejected.")
                if data["type"] == "ping":
                    continue

            if "message" not in data:
                continue

            msg = data["message"]
            if msg["event_class"] == "Post":
                # New post created. Analyze it.
                user_link = msg["object"]["user_link"]
                user_re = re.search(r'^https?:\/\/([a-z.]+)\/users\/([0-9]+)', user_link)

                user = (user_re.group(0), user_re.group(1),
                        msg["object"]["username"])

                post_tuple = (msg["object"]["title"], msg["object"]["body"], user)
                analyze_post(post_tuple)

            if msg["event_class"] == "Feedback":
                # Updates on feedback. Check if over threshold.
                post_id = msg["object"]["post_id"]
                feedbacks = get_feedback_on_post(post_id)
                is_over_thres = feedback_over_threshold(feedbacks)
                if is_over_thres is None:
                    # Not yet.
                    continue

                # Fetch post to be learned.
                post_tuple = get_post(post_id)
                learn_post(post_tuple, is_over_thres)
        except RuntimeError:
            # Severe errors
            raise
        except KeyboardInterrupt:
            # User decides to exit.
            ws.close()
            return None
        except Exception:
            # Reconnect.
            try:
                ws.close()
            except Exception:
                pass
            ws = init_ms_ws()


def feedback_over_threshold(feedbacks):
    """ Determine if feedback is over tp or fp threshold. """
    # Argument: the list returned by get_feedback_on_post()
    # Returns: None if not, True if tp and False if fp

    tp_count = 0
    fp_count = 0
    naa_count = 0
    for _, feedback in feedbacks:
        if feedback.startswith("tp"):
            tp_count += 1
        if feedback.startswith("fp"):
            fp_count += 1
        if feedback.startswith("naa") or feedback.startswith("ignore"):
            naa_count += 1

    w_tp_count = tp_count + naa_count * Config.naa_bias
    w_fp_count = fp_count + naa_count * (1 - Config.naa_bias)

    if (w_fp_count == 0) and (w_tp_count >= Config.un_thres):
        return True
    if (w_tp_count == 0) and (w_fp_count >= Config.un_thres):
        return False

    if w_tp_count and w_fp_count:
        # Controversial posts
        if (w_tp_count / w_fp_count) >= Config.co_thres:
            return True
        if (w_fp_count / w_tp_count) >= Config.co_thres:
            return False

    return None  # Not yet


def naive_tokenizer(post_tuple):
    """ Naive tokenizer, splitting string at whitespace. """
    # Argument: the tuple returned by get_post() or ms_ws_listener()
    # Returns: tokenized string list

    tokenized_title = post_tuple[0].split(" ")
    tokenized_body = post_tuple[1].split(" ")
    # Make unified_user_site_id unique from other potential tokens
    # by whitespace and other identifiable substrings
    # post[2] == (user_site, user_id, user_name)
    unified_user_site_id = "##usr## " + post_tuple[2][1] + " ::@:: " + post_tuple[2][0]
    tokenized_post = list()

    # Use SBPH wisely. The first token will be multiplied by 16,
    # the second by 8, the third by 4, and fourth by 2.
    # Hence the first token acts like uid black/white list
    tokenized_post.extend(unified_user_site_id)
    tokenized_post.extend(post_tuple[2][2])  # This is the username
    tokenized_post.extend(tokenized_title)
    tokenized_post.extend(tokenized_body)

    return tokenized_post


# Ad hoc code ahead.
# Please consider improving the following code to make them extensible.
def analyze_post(post_tuple):
    """ Call appropriate executables to analyze the post. """
    tokenized_post = naive_tokenizer(post_tuple)
    tokenized_post_str = "\n".join(tokenized_post) + "\n"
    tokenized_post_bytes = tokenized_post_str.encode("utf-8")

    sbph = subprocess.Popen(["vc/sbph"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ngram = subprocess.Popen(["vc/ngram"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bow = subprocess.Popen(["vc/bow"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sbph_nbc = subprocess.Popen(["cf/nbc", "--classify", "--data=dat/nbc/sbph.dat"],
                                stdin=sbph.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ngram_nbc = subprocess.Popen(["cf/nbc", "--classify", "--data=dat/nbc/ngram.dat"],
                                 stdin=ngram.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bow_nbc = subprocess.Popen(["cf/nbc", "--classify", "--data=dat/nbc/bow.dat"],
                               stdin=bow.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start
    sbph.stdin.write(tokenized_post_bytes)
    sbph.stdin.close()
    ngram.stdin.write(tokenized_post_bytes)
    ngram.stdin.close()
    bow.stdin.write(tokenized_post_bytes)
    bow.stdin.close()

    sbph_nbc_out = sbph_nbc.communicate()[0].decode("utf-8")
    ngram_nbc_out = ngram_nbc.communicate()[0].decode("utf-8")
    bow_nbc_out = bow_nbc.communicate()[0].decode("utf-8")

    print("Classify post: NT-SBPH-NBC: {}; NT-Ngram-NBC: {}; NT-BoW-NBC: {}".format(sbph_nbc_out,
                                                                                    ngram_nbc_out,
                                                                                    bow_nbc_out))


def learn_post(post_tuple, is_tp):
    """ Call appropriate executables to learn the post. """
    learn_arg_str = "--learn={}".format("T" if is_tp else "F")

    tokenized_post = naive_tokenizer(post_tuple)
    tokenized_post_str = "\n".join(tokenized_post) + "\n"
    tokenized_post_bytes = tokenized_post_str.encode("utf-8")

    sbph = subprocess.Popen(["vc/sbph"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ngram = subprocess.Popen(["vc/ngram"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bow = subprocess.Popen(["vc/bow"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sbph_nbc = subprocess.Popen(["cf/nbc", learn_arg_str, "--data=dat/nbc/sbph.dat"],
                                stdin=sbph.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ngram_nbc = subprocess.Popen(["cf/nbc", learn_arg_str, "--data=dat/nbc/ngram.dat"],
                                 stdin=ngram.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    bow_nbc = subprocess.Popen(["cf/nbc", learn_arg_str, "--data=dat/nbc/bow.dat"],
                               stdin=bow.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start
    sbph.stdin.write(tokenized_post_bytes)
    sbph.stdin.close()
    ngram.stdin.write(tokenized_post_bytes)
    ngram.stdin.close()
    bow.stdin.write(tokenized_post_bytes)
    bow.stdin.close()

    sbph_nbc_out = sbph_nbc.communicate()[0].decode("utf-8")
    ngram_nbc_out = ngram_nbc.communicate()[0].decode("utf-8")
    bow_nbc_out = bow_nbc.communicate()[0].decode("utf-8")

    print("Learn post: NT-SBPH-NBC: {}; NT-Ngram-NBC: {}; NT-BoW-NBC: {}".format(sbph_nbc_out,
                                                                                 ngram_nbc_out,
                                                                                 bow_nbc_out))


# Ad hoc code ends here
if __name__ == "__main__":
    ms_ws_listener()
