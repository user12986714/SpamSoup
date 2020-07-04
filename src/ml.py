# coding=utf-8

import re
import subprocess

import msg


ml_config = None
sw_config = list()


def config(cfg):
    """ Write ml_config. """
    global ml_config
    ml_config = cfg


def config_sw(sw):
    global sw_config
    sw_config = sw


def tokenize_string(string):
    """ Split a string into tokens. """
    # Argument: string
    # Returns: a list of tokens

    tokens = re.compile(r"[-\w']+").findall(string.lower())
    return [token for token in tokens if token not in sw_config]


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


def depth_first_exec(post_id, output_prefix, route, is_tp, prev_output):
    """ Perform depth first search on the route tree. """
    # Pass None for is_tp if classfying, True if learn as tp and False if learn as fp.

    output_prefix += "-" + route["exec"]
    exec_info = ml_config["exec"][route["exec"]]

    bin_with_args = [exec_info["bin"]]
    if exec_info["type"] == 0:
        pass
    elif exec_info["type"] == 1:
        if is_tp is None:
            bin_with_args.append("--classify")
        else:
            bin_with_args.append("--learn={}".format("T" if is_tp else "F"))
        bin_with_args.append("--data={}".format(route["data"]))

    proc = subprocess.Popen(bin_with_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_and_err = proc.communicate(input=prev_output)

    if out_and_err[1]:
        err_msg = "Errors occured when {}ing post {}: {}".format("classify" if is_tp is None else "learn", post_id, out_and_err[1].decode("utf-8").rstrip())
        msg.output(err_msg, msg.WARNING, tags=["Classify" if is_tp is None else "Learn", output_prefix])
        return  # Terminate this route

    if route["endpoint"]:
        out_msg = "Post {} {}: {}".format(post_id, "classified" if is_tp is None else "learned", out_and_err[0].decode("utf-8").rstrip())
        msg.output(out_msg, msg.INFO if is_tp is None else msg.DEBUG, tags=["Classify" if is_tp is None else "Learn", output_prefix])
        return

    for subroute in route["succ"]:
        depth_first_exec(post_id, output_prefix, subroute, is_tp, out_and_err[0])


def exec_ml(post_id, post_tuple, is_tp):
    """ Call appropriate executables to handle the post. """
    tokenized_post = naive_tokenizer(post_tuple)
    tokenized_post_str = "\n".join(tokenized_post) + "\n"
    tokenized_post_byte = tokenized_post_str.encode("utf-8")

    for route in ml_config["route"]:
        depth_first_exec(post_id, "NT", route, is_tp, tokenized_post_byte)
