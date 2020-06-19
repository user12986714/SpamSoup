# coding=utf-8

import re


def get_user(user_link, user_name):
    """ Get user tuple from user link and user name. """
    # Returns: (user_site, user_id, user_name)
    user_re = re.search(r'^(?:https?:)?\/\/([a-z.]+)\/users\/([0-9]+)', user_link)

    try:
        return (user_re.group(1), user_re.group(2), user_name)
    except AttributeError:
        # For a deleted user, the user name is not significant anyway
        return ("DELETED", "-2", "A deleted user")  # -1 is used by Community
