# Ubuntu with python3
FROM ubuntu:20.04

LABEL maintainer="princeb4d@gmail.com"

# 安装时区文件并设置默认时区
ENV TZ=Asia/Shanghai
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
  && apt-get update \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
  && apt-get install tzdata \
  && apt-get clean \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# 安装python3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
# 复制项目文件并启动监听程序
COPY . /app
RUN pip install -r /app/requirements.txt
CMD python /app/epdserv.py
EXPOSE 6868/tcp