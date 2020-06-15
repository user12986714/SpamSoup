#!/usr/bin/env python3
# coding=utf-8

import re
import sys
import pickle


def at_index(string, element_index):
    """ Get the string at the specified index of a list seperated by ',' """
    len_string = len(string)

    current_index = 0
    current_ptr = 0

    is_in_quote = False
    is_escaped = False

    while current_ptr < len_string and current_index < element_index:
        if not (is_in_quote or is_escaped) and string[current_ptr] == ",":
            current_index += 1
        if not is_escaped and string[current_ptr] in {r"'", r'"'}:
            is_in_quote = not is_in_quote
        if not is_escaped and string[current_ptr] == "\\":
            is_escaped = True
        elif is_escaped:
            is_escaped = False
        current_ptr += 1

    if current_ptr == len_string:
        raise RuntimeError("Bad string.")

    element_start = current_ptr

    while current_ptr < len_string and (is_in_quote or is_escaped or
                                        string[current_ptr] != ","):
        if not is_escaped and string[current_ptr] in {r"'", r'"'}:
            is_in_quote = not is_in_quote
        if not is_escaped and string[current_ptr] == "\\":
            is_escaped = True
        elif is_escaped:
            is_escaped = False
        current_ptr += 1

    return string[element_start:current_ptr]


def unescape(string):
    """ Unescape a string. """
    len_string = len(string)
    current_ptr = 0
    is_escaped = False

    unescaped_str = ""

    while current_ptr < len_string:
        if not is_escaped and string[current_ptr] == "\\":
            is_escaped = True
            current_ptr += 1
            continue
        unescaped_str += string[current_ptr]
        is_escaped = False
        current_ptr += 1

    return unescaped_str


def proc_posts(splitted_post_loc):
    """ Process posts and generate a dict accordingly. """
    skipped_posts = 0
    posts = dict()

    with open(splitted_post_loc, "r",
              encoding="utf-8", errors="ignore") as post_file:
        for line in post_file:
            if len(line) < 5:  # Certainly broken, and is not a post
                continue
            line = line.rstrip()

            post_id = at_index(line, 0)
            post_title = at_index(line, 1)
            post_body = at_index(line, 2)
            user_link = at_index(line, 8)
            user_name = at_index(line, 9)

            if "NULL" in {post_id, post_title, post_body,
                          user_link, user_name}:
                # Missing info.
                skipped_posts += 1
                continue

            try:
                post_title = unescape(post_title[1:-1])
                post_body = unescape(post_body[1:-1])
                user_link = unescape(user_link[1:-1])
                user_name = unescape(user_name[1:-1])
            except IndexError:
                # Bad post format.
                skipped_posts += 1
                continue

            user_re = re.search(r'(?:https?:)?\/\/([a-z.]+)\/users\/([0-9]+)', user_link)
            if user_re is None:
                # Missing info.
                skipped_posts += 1
                continue
            user = (user_re.group(1), user_re.group(2), user_name)

            posts[post_id] = dict()
            posts[post_id]["post"] = (post_title, post_body, user)
            posts[post_id]["feedback"] = list()

    return (skipped_posts, posts)


def proc_feedbacks(splitted_feedback_loc, posts_dict):
    """ Process feedbacks and add them to the posts dict. """
    skipped_feedbacks = 0

    with open(splitted_feedback_loc, "r",
              encoding="utf-8", errors="ignore") as feedback_file:
        for line in feedback_file:
            if len(line) < 5:
                continue
            line = line.rstrip()

            post_id = at_index(line, 5)
            from_user = at_index(line, 2)
            feedback_type = at_index(line, 4)

            if "NULL" in {post_id, from_user, feedback_type}:
                # Missing info
                skipped_feedbacks += 1
                continue

            try:
                from_user = unescape(from_user[1:-1])
                feedback_type = unescape(feedback_type[1:-1])
            except IndexError:
                # Bad feedback format.
                skipped_feedbacks += 1
                continue

            if post_id not in posts_dict:
                # The post the feedback is skipped
                skipped_feedbacks += 1
                continue

            feedback = (from_user, feedback_type)
            posts_dict[post_id]["feedback"].append(feedback)

    return (skipped_feedbacks, posts_dict)


def join():
    """ Join posts and feedbacks. """
    # Three command line arguments shall be passed,
    # The first shall be the path to posts processed by split.py
    # The second shall be the path to feedbacks processed by split.py
    # The third shall be the path to where the output pickle is to be stored

    print("Start processing posts.")
    posts = proc_posts(sys.argv[1])
    print("Skipped {} posts.".format(posts[0]))
    print("Start processing feedbacks.")
    joined_posts = proc_feedbacks(sys.argv[2], posts[1])
    print("Skipped {} feedbacks.".format(joined_posts[0]))
    print("Start dumping the pickle.")
    with open(sys.argv[3], "wb") as pickle_file:
        pickle.dump(joined_posts[1], pickle_file)


if __name__ == "__main__":
    join()
