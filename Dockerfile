FROM python:3.11-slim-bullseye

# install git
RUN apt-get update && \
    apt-get install git ffmpeg -y

    # install pip
RUN pip install --upgrade pip

# install whisper
RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install moviepy

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]