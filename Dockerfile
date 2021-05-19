# Ubuntu with python3
FROM ubuntu:20.04

LABEL maintainer="princeb4d@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app
RUN pip install -r /app/requirements.txt
CMD python /app/epdserv.py
EXPOSE 6868/tcp