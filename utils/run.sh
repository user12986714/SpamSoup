#!/usr/bin/sh

ON_BRANCH="prod"
DATA_BRANCH="instance-name"

wait_until_ready(){
    while ! [ -f "READY" ]; do
        sleep 5
    done
}

wait_until_ready
while :; do
    git pull upstream "${ON_BRANCH}"
    git checkout "${ON_BRANCH}"
    sh build.sh
    python3 -u ./bin/glue.py --config=cfg.json --stopword=sw.json | stdbuf -o0 python3 ws_tee.py
    cd data
    if ! git branch | grep "${DATA_BRANCH}"; then
        git checkout master
        git branch "${DATA_BRANCH}"
        git push --set-upstream origin "${DATA_BRANCH}"
    fi
    git checkout "${DATA_BRANCH}"
    git add .
    git commit -m "$(date +%s)"
    git push
    cd ..
done
