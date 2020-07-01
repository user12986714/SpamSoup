#!/usr/bin/env python3
# coding=utf-8

import sys
import threading

# Note: this script need pip3 package SimpleWebSocketServer
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


clients = list()
clients_rw_lock = threading.Lock()

key = "simple key"
host = "127.0.0.1"
port = 12345
interval = 0.5


class WSServer(WebSocket):
    def handleConnected(self):
        self.sendMessage("welcome")

    def handleMessage(self):
        if self.data == key:
            with clients_rw_lock:
                clients.append(self)
            sys.stderr.write("{} authenticated.\n".format(self.address))
            self.sendMessage("confirmed")
        else:
            self.sendMessage("rejected")
            self.sendClose()

    def handleClose(self):
        try:
            with clients_rw_lock:
                clients.remove(self)
        except Exception:
            pass


def tee_input():
    for line in sys.stdin:
        if tee_to_stdout:
            sys.stdout.write(line)
        with clients_rw_lock:
            for client in clients:
                client.sendMessage(line.rstrip())


def ws_tee():
    ws_server = SimpleWebSocketServer(host, port, WSServer, interval)
    threading.Thread(name="tee_input", target=tee_input, daemon=True).start()
    ws_server.serveforever()


if __name__ == "__main__":
    tee_to_stdout = "--no-stdout" not in sys.argv
    ws_tee()
