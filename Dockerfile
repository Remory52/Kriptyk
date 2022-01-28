FROM ubuntu:18.04
COPY requirements.txt requirements.txt
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install build-essential libssl-dev libffi-dev -y
RUN apt install ffmpeg -y
RUN apt install python3-pip -y && pip3 install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ home/
WORKDIR /home
CMD [ "python3", "main.py"]