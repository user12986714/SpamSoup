FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache build-base
#RUN adduser -D spamsoup
RUN pip install requests websocket-client SimpleWebSocketServer
RUN mkdir -p /src/bin /src/src /src/data

ADD build.sh /src/
ADD run.sh /src/
ADD bin /src/bin/
ADD src /src/src/
ADD data /src/data/
ADD cfg.json /src/

WORKDIR /src
RUN /src/build.sh

RUN apk del build-base
RUN rm -rf /var/cache/apk

CMD ["sh", "run.sh"]
