#!/usr/bin/env python3
# coding=utf-8

import sys
import math
import pickle

import ml


def manual_op(joined_posts, need_manual_op):
    print("Feedbacks on {} posts do not reach the threshold. ".format(len(need_manual_op)) +
          "You may skip them, mark them all as a certain type, " +
          "manually tag some of them or manually tag all of them.")
    print("Would you like to start tagging them(Y), marking as " +
          "tp(T), fp(F) or skip(Any)? (Y/T/F/Any)")
    user_choice = sys.stdin.readline().rstrip().upper()

    if user_choice not in {"Y", "T", "F"}:
        for post_id in need_manual_op:
            del joined_posts[post_id]
        print("{} posts skipped.".format(len(need_manual_op)))
        return joined_posts

    if user_choice in {"T", "F"}:
        for post_id in need_manual_op:
            joined_posts[post_id]["tag"] = (user_choice == "T")
        return joined_posts

    skip_all = False
    num_posts_skipped = 0
    for post_id in need_manual_op:
        if skip_all:
            del joined_posts[post_id]
            num_posts_skipped += 1
            continue
        print("Post tuple for post {}:".format(post_id))
        print(joined_posts[post_id]["post"])
        print("Existing feedbacks:")
        print(joined_posts[post_id]["feedback"])
        print("Mark as tp(T), fp(F), skip(S), or skip all(Any)? (T/F/S/Any)")
        user_choice = sys.stdin.readline().rstrip().upper()
        if user_choice not in {"T", "F", "S"}:
            skip_all = True
            del joined_posts[post_id]
            num_posts_skipped += 1
            continue
        if user_choice == "S":
            del joined_posts[post_id]
            num_posts_skipped += 1
            continue
        joined_posts[post_id]["tag"] = (user_choice == "T")

    print("{} posts skipped.".format(num_posts_skipped))
    return joined_posts


def learn():
    with open(sys.argv[1], "rb") as pickle_file:
        joined_posts = pickle.load(pickle_file)

    assert isinstance(joined_posts, dict)

    need_manual_op = list()
    for post_id in joined_posts:
        is_over_thres = ml.feedback_over_threshold(joined_posts[post_id]["feedback"])
        if is_over_thres is None:
            need_manual_op.append(post_id)
        else:
            joined_posts[post_id]["tag"] = is_over_thres

    if need_manual_op:
        joined_posts = manual_op(joined_posts, need_manual_op)

    if "balanced" in sys.argv:
        print("Start separating tp/fp posts.")
        # Seperate tp and fp posts
        tp_posts = {x: joined_posts[x] for x in joined_posts if joined_posts[x]["tag"]}
        fp_posts = {x: joined_posts[x] for x in joined_posts if not joined_posts[x]["tag"]}
        print("tp/fp separated.")

        len_tp = len(tp_posts)
        len_fp = len(fp_posts)

        if len_tp > len_fp:
            list_tp_index = [x for x in tp_posts]
            list_tp_index.sort(key=int)

            print("Start removing {} keys from tp.".format(len_tp - len_fp))
            # Remove the ealiest keys
            for key in range(len_tp - len_fp):
                del tp_posts[list_tp_index[key]]

        if len_tp < len_fp:
            list_fp_index = [x for x in fp_posts]
            list_fp_index.sort(key=int)

            print("Start removing {} keys from fp.".format(len_fp - len_tp))
            # Remove the ealiest keys
            for key in range(len_fp - len_tp):
                del fp_posts[list_fp_index[key]]

        if len_tp != len_fp:
            print("Start merging tp/fp.")
            tp_posts.update(fp_posts)
            joined_posts = tp_posts

    if "bias-66" in sys.argv:
        print("Start separating tp/fp posts.")
        # Seperate tp and fp posts
        tp_posts = {x: joined_posts[x] for x in joined_posts if joined_posts[x]["tag"]}
        fp_posts = {x: joined_posts[x] for x in joined_posts if not joined_posts[x]["tag"]}
        print("tp/fp separated.")

        len_tp = len(tp_posts)
        len_fp = len(fp_posts)
        expected_len_tp = math.floor(len_fp * 0.66 / 0.34)

        if len_tp > expected_len_tp:
            list_tp_index = [x for x in tp_posts]
            list_tp_index.sort(key=int)

            print("Start removing {} keys from tp.".format(len_tp - expected_len_tp))
            # Remove the ealiest keys
            for key in range(len_tp - expected_len_tp):
                del tp_posts[list_tp_index[key]]
        else:
            expected_len_fp = math.floor(len_tp * 0.34 / 0.66)
            if len_fp > expected_len_fp:
                print("Start removing {} keys from fp.".format(len_fp - expected_len_fp))
                # Remove the ealiest keys
                for key in range(len_fp - expected_len_fp):
                    del fp_posts[list_fp_index[key]]

        print("Start merging tp/fp.")
        tp_posts.update(fp_posts)
        joined_posts = tp_posts

    num_posts_learned = 0
    num_total_posts = len(joined_posts)
    print("Start learning {} posts.".format(num_total_posts))

    for post_id in joined_posts:
        ml.exec_ml("LEARN", joined_posts[post_id]["post"], joined_posts[post_id]["tag"])
        num_posts_learned += 1
        if num_posts_learned % 500 == 0:
            print("{} posts out of {} learned.".format(num_posts_learned, num_total_posts))


if __name__ == "__main__":
    learn()
