FROM python:3.8.12
WORKDIR /backend
ADD ./requirements.txt /backend
RUN cat /etc/apt/sources.list > /etc/apt/sources.list.bak && sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list && apt-get -y update \
    && apt-get install 'ffmpeg' \
    'libsm6' \ 
    'libxext6'  -y
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV LANG C.UTF-8
EXPOSE 8000