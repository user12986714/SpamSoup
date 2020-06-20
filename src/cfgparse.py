# coding=utf-8

import json


def parse(cfg_file):
    """ Parse config. """
    # There is no try-except block here, and is intended.
    # The program should stop and print out the traceback as
    # it won't work properly with invalid config anyway.
    with open(cfg_file, "r", encoding="utf-8") as cfg_stream:
            cfg = json.load(cfg_stream)

    output_levels = {"VERBOSE": 0, "DEBUG": 1, "INFO": 2,
                     "WARNING": 3, "ERROR": 4, "CRITICAL": 5}
    config = dict()

    assert isinstance(cfg["io"]["dest"], list)

    config["msg"] = {"dest": list()}
    for file in cfg["io"]["dest"]:
        assert isinstance(file["path"], str)
        assert isinstance(file["level"], str)

        assert file["level"].upper() in output_levels

        config["msg"]["dest"].append({"path": file["path"],
                                      "level": output_levels[file["level"].upper()]})

    assert isinstance(cfg["ms"]["ms_host"], str)
    assert isinstance(cfg["ms"]["ws_host"], str)
    assert isinstance(cfg["ms"]["api_key"], str)
    assert isinstance(cfg["ms"]["ws_max_retry"], int)
    assert isinstance(cfg["ms"]["ws_retry_sleep"], int)
    assert isinstance(cfg["ms"]["ws_timeout"], int)

    assert cfg["ms"]["ms_host"]
    assert cfg["ms"]["ws_host"]
    assert cfg["ms"]["api_key"]
    assert cfg["ms"]["ws_max_retry"] > -2  # >= -1
    assert cfg["ms"]["ws_retry_sleep"] > -1  # >= 0
    assert cfg["ms"]["ws_timeout"] > 0

    config["ws"] = {"ws_host": cfg["ms"]["ws_host"],
                    "ms_host": cfg["ms"]["ms_host"],
                    "api_key": cfg["ms"]["api_key"],
                    "max_retry": cfg["ms"]["ws_max_retry"],
                    "retry_sleep": cfg["ms"]["ws_retry_sleep"],
                    "timeout": cfg["ms"]["ws_timeout"]}

    config["msapi"] = {"ms_host": cfg["ms"]["ms_host"],
                       "api_key": cfg["ms"]["api_key"]}

    assert isinstance(cfg["ml"]["feedback"]["naa_to_tp"], float)
    assert isinstance(cfg["ml"]["feedback"]["naa_to_fp"], float)
    assert isinstance(cfg["ml"]["feedback"]["un_thres"], float)
    assert isinstance(cfg["ml"]["feedback"]["co_thres"], float)

    config["ml"] = {"feedback": {"naa_to_tp": cfg["ml"]["feedback"]["naa_to_tp"],
                                 "naa_to_fp": cfg["ml"]["feedback"]["naa_to_fp"],
                                 "un_thres": cfg["ml"]["feedback"]["un_thres"],
                                 "co_thres": cfg["ml"]["feedback"]["co_thres"]}}

    return config
