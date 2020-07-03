#!/usr/bin/sh

ON_BRANCH="prod"
DATA_BRANCH="instance-name"

CFG_AT="config-json-location"
SW_AT="stopword-json-location"

USER_STR="user-name"
INST_STR="inst-name"

wait_until_ready(){
    while ! [ -f "READY" ]; do
        sleep 5
    done
}

upload_data(){
    cd data
    if ! git branch | grep "${DATA_BRANCH}" > /dev/null; then
        git checkout master
        git branch "${DATA_BRANCH}"
        git push --set-upstream origin "${DATA_BRANCH}"
    fi
    git checkout "${DATA_BRANCH}"
    git add .
    git commit -m "$(date +%s)"
    git push
    cd ..
}

wait_until_ready
while :; do
    python3 -u ./bin/glue.py "--config=${CFG_AT}" "--stopword=${SW_AT}" "--user=${USER_STR}" "--inst=${INST_STR}" | stdbuf -o0 python3 ws_tee.py
    upload_data
done
