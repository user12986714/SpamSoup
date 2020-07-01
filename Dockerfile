FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache build-base
#RUN adduser -D spamsoup
RUN pip install requests websocket-client
RUN mkdir -p /src/bin /src/src /src/utils

ADD build.sh /src/
ADD bin /src/bin/
ADD src /src/src/
ADD utils /src/utils
ADD cfg.json /src/

WORKDIR /src
RUN /src/build.sh

RUN apk del build-base
RUN rm -rf /var/cache/apk

CMD ["python3", "./bin/glue.py", "--config=cfg.json"]