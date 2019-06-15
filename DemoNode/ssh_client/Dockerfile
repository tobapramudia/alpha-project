FROM alpine

ENV TZ='Asia/Jakarta'

ENV SSH_SERVER='127.0.0.1'

ADD . /app

WORKDIR /app

RUN apk add --no-cache --virtual --no-progress -q \
    openssh-client \
    tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && chmod +x run.sh

CMD ./run.sh $SSH_SERVER