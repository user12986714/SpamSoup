import more_itertools


def unique_features(out_and_err):
    """ Remove duplicate features. """
    if out_and_err[1]:
        return out_and_err
    all_features = out_and_err[0].decode("utf-8").rstrip().split("\n")
    reduced_features = more_itertools.unique_everseen(all_features)
    return (("\n".join(reduced_features) + "\n").encode("utf-8"), out_and_err[1])
