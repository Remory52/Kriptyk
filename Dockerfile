FROM ubuntu:latest
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install ffmpeg -y
RUN apt install python3-pip -y
RUN pip install discord
RUN pip install python-dotenv
RUN pip install youtube-dl
RUN pip install pynacl
COPY ./ home/
WORKDIR /home
CMD [ "python3", "main.py"]