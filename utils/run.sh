#!/usr/bin/sh

wait_until_ready(){
    while ! [ -f "READY" ]; do
        sleep 5
    done
}

rescue_docker(){
    touch "WARNING"
    sleep infinity
}

wait_until_ready
python3 -u ./bin/glue.py --config=cfg.json --stopword=sw.json | stdbuf -o0 python3 ws_tee.py
rescue_docker
