FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache build-base
RUN apk add --no-cache coreutils openssh-client git
#RUN adduser -D spamsoup
RUN pip install requests websocket-client SimpleWebSocketServer
RUN mkdir -p /src/bin /src/src /src/data

RUN mkdir -p /root/.ssh
RUN touch /root/.ssh/known_hosts

ADD build.sh /src/
ADD run.sh /src/
ADD src /src/src/
ADD data /src/data/
ADD cfg.json /src/
ADD sw.json /src/
ADD ws_tee.py /src/
ADD deploy_key /src/

WORKDIR /src
RUN sh build.sh
RUN apk del build-base
RUN rm -rf /var/cache/apk

CMD ["sh", "run.sh"]
