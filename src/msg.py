# coding=utf-8

import sys
import time


VERBOSE = 0
DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4
CRITICAL = 5

levels = ["VERBOSE", "DEBUG", "INFO",
          "WARNING", "ERROR", "CRITICAL"]


# Special destination handlers.
def print_stdout(msg):
    """ Print to stdout handler. """
    sys.stdout.write(msg)


def print_stderr(msg):
    """ Print to stderr handler. """
    sys.stderr.write(msg)


special_dest = {"\\stdout//": print_stdout,
                "\\stderr//": print_stderr}

msg_config = None


def config(cfg):
    """ Write msg_config. """
    global msg_config
    msg_config = cfg


def add_dest(dest_str, out_level):
    """ Add an output destination. """
    global msg_config

    msg_config["dest"].append({"path": dest_str,
                               "level": out_level})


def rm_dest(dest_str):
    """ Remove an output destination. """
    global msg_config

    for dest in msg_config["dest"]:
        if dest["path"] == dest_str:
            del dest


def output(message, level, tags=None, exclude=None):
    """ Output a message. """
    msg_to_output = "[{:.3f}] ".format(time.time())

    if tags:
        for tag in tags:
            msg_to_output += "[{}] ".format(tag)

    msg_to_output += "<{}> {}\n".format(levels[level],
                                       message)
    for output_dest in msg_config["dest"]:
        if level < output_dest["level"]:
            # Not reaching output level.
            continue

        if exclude:
            if output_dest["path"] in exclude:
                # Excluded.
                continue

        print_to(output_dest["path"], msg_to_output)


def print_to(output_dest, msg):
    """ Print a message to a destination. """
    if output_dest in special_dest:
        special_dest[output_dest](msg)
        return

    with open(output_dest, "a", encoding="utf-8") as output_stream:
        output_stream.write(msg)

