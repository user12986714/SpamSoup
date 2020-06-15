#!/usr/bin/env python3
# coding=utf-8

import sys


def split_line(line):
    """ Split a line into several elements. """
    if line[0] != "(" or line[-1] != ")":
        raise RuntimeError("Bad line.")

    len_line = len(line)

    element_list = list()
    previous_delimeter = 1
    current_ptr = 1

    is_in_quote = False
    is_escaped = False

    while current_ptr < len_line:
        if not is_in_quote and not is_escaped and line[current_ptr] == ")":
            element_list.append(line[previous_delimeter:current_ptr])
            current_ptr += 3
            previous_delimeter = current_ptr
            continue
        if not is_escaped and line[current_ptr] in {r"'", r'"'}:
            is_in_quote = not is_in_quote
        if not is_escaped and line[current_ptr] == "\\":
            is_escaped = True
        elif is_escaped:
            is_escaped = False
        current_ptr += 1

    return element_list

def split():
    """ Split lines preprocessed by a gen*.sh script. """
    str_list = sys.stdin.readlines()
    element_list = list()

    for line in str_list:
        element_list.extend(split_line(line.rstrip()))

    for element in element_list:
        print(element)


if __name__ == "__main__":
    split()
