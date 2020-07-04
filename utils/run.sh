#!/usr/bin/sh

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

setup_branch(){
    # !!!!! WARNING !!!!!
    # The following command is vulnerable to MitM attack.
    # If this is an issue, remove the following line and
    # add trusted hosts manually.
    ssh-keyscan -H github.com >> ~/.ssh/known_hosts

    cd data
    git pull origin master
    if ! git checkout -f "${DATA_BRANCH}"; then
        git checkout -f master
        git branch "${DATA_BRANCH}"
        git checkout "${DATA_BRANCH}"
        git push --set-upstream origin "${DATA_BRANCH}"
    else
        git pull origin "${DATA_BRANCH}"
    fi
    cd ..
}

upload_data(){
    cd data
    git add .
    git commit -m "$(date +%s)"
    git push
    cd ..
}

check_if_stop(){
    if [ -f "STOP" ]; then
        exit
    fi
}

wait_until_ready
setup_branch
while :; do
    python3 -u ./bin/glue.py "--config=${CFG_AT}" "--stopword=${SW_AT}" "--user=${USER_STR}" "--inst=${INST_STR}" | stdbuf -o0 python3 ws_tee.py
    upload_data
    check_if_stop
done
