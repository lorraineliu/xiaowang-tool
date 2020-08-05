FROM ubuntu:latest

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ARG access_key_id
ARG access_key_secret
ARG region_id
ARG instance_id

ENV access_key_id=${access_key_id}
ENV access_key_secret=${access_key_secret}
ENV region_id=${region_id}
ENV instance_id=${instance_id}

RUN apt update && apt upgrade -y && apt install python \
    curl \
    cron \
    git \
    vim -y
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Install Application into container:
RUN set -ex && mkdir /app
WORKDIR /app

RUN pip --no-cache-dir install click \
    python-crontab \
    aliyun-python-sdk-core \
    aliyun-python-sdk-vpc

# 添加源码
ADD src /app

# Setup cron job
# Run the command on container startup
#CMD python cronjob.py init-common-bandwidth-cronjob ${access_key_id} \
#    ${access_key_secret} \
#    ${region_id} \
#    ${instance_id} && tail -f /var/log/cron.log
CMD tail -f /var/log/cron.log
