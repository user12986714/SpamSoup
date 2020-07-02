FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache build-base
#RUN adduser -D spamsoup
RUN pip install requests websocket-client SimpleWebSocketServer
RUN mkdir -p /src/bin /src/src /src/data

ADD build.sh /src/
ADD run.sh /src/
ADD src /src/src/
ADD data /src/data/
ADD cfg.json /src/
ADD sw.json /src/

WORKDIR /src
CMD ["sh", "run.sh"]
