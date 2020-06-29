FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache build-base
#RUN adduser -D spamsoup
RUN pip install requests websocket-client
RUN mkdir -p /src/bin /src/src /src/utils

ADD build.sh /src/
ADD bin /src/bin/
ADD src /src/src/
ADD utils /src/utils

WORKDIR /src
RUN /src/build.sh

RUN apk del build-base
RUN rm -rf /var/cache/apk

WORKDIR /src
CMD ["python3", "glue.py", "--config=cfg.json"]
