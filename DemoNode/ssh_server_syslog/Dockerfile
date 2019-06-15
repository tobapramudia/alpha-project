FROM alpine

ENV TZ='Asia/Jakarta'

ENV SYSLOG_SERVER='127.0.0.1'

COPY entrypoint.sh /sbin/entrypoint.sh

RUN apk add --no-cache --virtual --no-progress -q \
    openssh-client \
    openssh-server \
    rsyslog \
    tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && chmod +x /sbin/entrypoint.sh

RUN echo "root:Docker!" | chpasswd

ENTRYPOINT ["/sbin/entrypoint.sh"]

CMD exec /usr/sbin/sshd -f /etc/ssh/sshd_config -D