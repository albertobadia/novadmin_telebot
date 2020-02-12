FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i es_AR -c -f UTF-8 -A /usr/share/locale/locale.alias es_AR.UTF-8
ENV LANG es_AR.utf8

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD python server.py
