FROM python:2.7-alpine

ADD . /app

ENV server='http://locahost/'

WORKDIR /app

EXPOSE 541

CMD python app.py --server $server