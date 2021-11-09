FROM python:3.9.7-slim-buster
COPY . /vbot
WORKDIR /vbot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt upgrade -y && apt -qq install -y git wget pv jq wget python3-dev ffmpeg pkg-config
RUN apt install -y  libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
RUN pip3 install -r requirements.txt
RUN pip3 install av --no-binary av
CMD ["bash", "run.sh"]
