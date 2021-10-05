FROM ubuntu:18.04
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install build-essential libssl-dev libffi-dev -y
RUN apt install ffmpeg -y
RUN apt install python3-pip -y
RUN pip3 install discord
RUN pip3 install python-dotenv
RUN pip3 install youtube-dl
RUN pip3 install pynacl
COPY ./ home/
WORKDIR /home
CMD [ "python3", "main.py"]