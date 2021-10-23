FROM ubuntu:18.04
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install build-essential libssl-dev libffi-dev -y
RUN apt install ffmpeg -y
RUN apt install python3-pip -y && pip3 install --upgrade pip
RUN pip3 install discord && pip3 install youtube-dl
RUN pip3 install cryptography && pip3 install pyopenssl && pip3 install python-dotenv
RUN pip3 install pynacl && pip3 install google
COPY ./ home/
WORKDIR /home
CMD [ "python3", "main.py"]