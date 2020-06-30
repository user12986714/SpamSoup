#!/usr/bin/env python3
# coding=utf-8

import sys
import time
import json
import websocket

from verinfo import ver_info

import msg
import msapi
import dataproc
import ml
import cfgparse


config_ws = None


def conn_ms_ws():
    """ Connect to metasmoke websocket. """
    failure_count = 0
    while True:
        try:
            ws = websocket.create_connection(config_ws["ws_host"],
                                             origin=config_ws["ms_host"])
            idf = r'{"channel": "ApiChannel",' +\
                  r'"key": "{}",'.format(config_ws["api_key"]) +\
                  r'"events": "feedbacks#create;posts#create"}'
            payload = json.dumps({"command": "subscribe", "identifier": idf})

            ws.send(payload)
            ws.settimeout(config_ws["timeout"])
            return ws
        except Exception as e:
            msg.output(str(e), msg.WARNING, tags=["WebSocket"])
            failure_count += 1
            if config_ws["max_retry"] > -1:  # -1 is unlimited.
                if failure_count > config_ws["max_retry"]:
                    msg.output("Cannot connect to Metasmoke WebSocket.",
                               msg.ERROR, tags=["WebSocket"])
                    raise RuntimeError("Cannot connect to Metasmoke WebSocket.")

            if config_ws["retry_sleep"]:
                time.sleep(config_ws["retry_sleep"])


def ms_ws_listener():
    """ Metasmoke websocket listener. """
    already_learned_posts = dict()
    ws = conn_ms_ws()
    msg.output("Connected to Metasmoke WebSocket.", msg.DEBUG, tags=["WebSocket"])
    while True:
        try:
            resp = ws.recv()
            try:
                data = json.loads(resp)
            except Exception:
                msg.output("Metasmoke WebSocket response is invalid.",
                           msg.WARNING, tags=["WebSocket"])
                continue

            if "type" in data:
                if data["type"] == "welcome":
                    msg.output("Metasmoke WebSocket welcome message received.",
                               msg.DEBUG, tags=["WebSocket"])
                    continue
                if data["type"] == "reject_subscription":
                    msg.output("Metasmoke WebSocket subscription rejected.",
                               msg.CRITICAL, tags=["WebSocket"])
                    raise RuntimeError("Metasmoke WebSocket subscription rejected.")
                if data["type"] == "ping":
                    msg.output("Metasmoke WebSocket ping received.",
                               msg.VERBOSE, tags=["WebSocket"])
                    continue

            if "message" not in data:
                msg.output("Metasmoke WebSocket response does not contain message field.",
                           msg.DEBUG, tags=["WebSocket"])
                continue

            message = data["message"]
            msg.output("Metasmoke WebSocket message received.",
                       msg.VERBOSE, tags=["WebSocket"])

            if message["event_class"] == "Post":
                # New post created. Analyze it.
                post_id = message["object"]["id"]
                msg.output("New post {} received from Metasmoke WebSocket.".format(post_id),
                           msg.INFO, tags=["WebSocket", "Post"])
                
                user = dataproc.get_user(message["object"]["user_link"],
                                         message["object"]["username"])
                msg.output("Author of post {} extracted as {}.".format(post_id, user),
                           msg.VERBOSE, tags=["Post"])

                post_tuple = (message["object"]["title"],
                              message["object"]["body"], user)
                msg.output("Post tuple for {} formed as {}.".format(post_id, post_tuple),
                           msg.VERBOSE, tags=["Post"])

                ml.exec_ml(post_id, post_tuple, None)

            if message["event_class"] == "Feedback":
                # Updates on feedback. Check if over threshold.
                post_id = message["object"]["post_id"]
                msg.output("New feedback event for post {} received from Metasmoke WebSocket.".format(post_id),
                           msg.DEBUG, tags=["WebSocket", "Feedback"])

                time.sleep(1)  # This is needed due to an issue in MS API.

                try:
                    feedbacks = msapi.get_feedback(post_id)
                except ValueError as e:
                    msg.output("{}".format(e), msg.WARNING, tags=["HTTP", "Feedback"])
                    continue
                msg.output("Feedbacks for post {} fetched from Metasmoke HTTP API as {}.".format(post_id, feedbacks),
                           msg.VERBOSE, tags=["HTTP", "Feedback"])

                is_over_thres = ml.feedback_over_threshold(post_id, feedbacks)
                if is_over_thres is None:
                    # Not yet.
                    msg.output("Feedbacks for post {} are insufficient.".format(post_id),
                               msg.DEBUG, tags=["Feedback"])
                    continue

                if post_id in already_learned_posts:
                    if already_learned_posts[post_id] == is_over_thres:
                        msg.output("Post {} already learned as {}.".format(post_id,
                                                                           "tp" if is_over_thres else "fp"),
                                   msg.DEBUG, tags=["Feedback"])
                        continue
                    else:
                        msg.output("Post {} already learned as {}, but feedbacks indicate that it is {}.".format(post_id,
                                                                                                                 "fp" if is_over_thres else "tp",
                                                                                                                 "tp" if is_over_thres else "fp"),
                                   msg.INFO, tags=["Feedback", "Learn-incorrect"]);

                msg.output("Post {} registered as {} by feedbacks.".format(post_id,
                                                                           "tp" if is_over_thres else "fp"),
                           msg.INFO, tags=["Feedback"])

                # Fetch post to be learned.
                try:
                    post_tuple = msapi.get_post(post_id)
                except ValueError as e:
                    msg.output("{}".format(e), msg.WARNING, tags=["HTTP", "Post"])
                    continue
                msg.output("Post tuple for {} fetched from Metasmoke HTTP API as {}.".format(post_id, post_tuple),
                           msg.VERBOSE, tags=["HTTP", "Post"])

                already_learned_posts[post_id] = is_over_thres
                ml.exec_ml(post_id, post_tuple, is_over_thres)
        except RuntimeError as e:
            # Severe errors
            msg.output("{}".format(e), msg.ERROR, tags=["Framework"])
            raise
        except KeyboardInterrupt:
            msg.output("User enforced program termination.",
                       msg.DEBUG, tags=["Framework"])
            ws.close()
            return None
        except Exception as e:
            msg.output("{}".format(e), msg.WARNING, tags=["Framework"])
            # Reconnect.
            try:
                ws.close()
            except Exception:
                pass
            ws = conn_ms_ws()
            msg.output("Reconnected to Metasmoke WebSocket.",
                       msg.DEBUG, tags=["WebSocket"])


if __name__ == "__main__":
    cfg_arg = [x for x in sys.argv if x.startswith("--config=")]
    if len(cfg_arg) != 1:
        cfg_location = "cfg.json"  # Default
    else:
        cfg_location = cfg_arg[0].split("=", 1)[1]

    config = cfgparse.parse(cfg_location)

    startup_str = "SpamSoup {major} ({alias}) started at {major}.{minor} on {user}/{inst}."
    startup_str = startup_str.format(major=ver_info["major"],
                                     alias=ver_info["alias"],
                                     minor=ver_info["minor"],
                                     user=ver_info["user"],
                                     inst=ver_info["inst"])

    config_ws = config["ws"]
    msg.config(config["msg"])
    msapi.config(config["msapi"])
    ml.config(config["ml"])

    msg.output(startup_str, msg.INFO, tags=["Framework"])
    ms_ws_listener()
