FROM python:2.7-alpine

ADD . /app

ENV FLASK_APP="app"
ENV FLASK_DEBUG="1"

WORKDIR /app

RUN cp app.clean.db app.db

RUN pip install Flask --no-cache-dir -q

EXPOSE 5000

CMD ["flask" , "run", "--host", "0.0.0.0"]