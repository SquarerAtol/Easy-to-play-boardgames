# base image
FROM python:3.11.9

# apt-get version, install sqlite3
# pip version
# library
RUN apt-get update && \
    apt-get install -y sqlite3 libsqlite3-dev && \
	rm -rf /var/lib/apt/lists/*

# container working dir
WORKDIR /usr/app/

# requirements 복사, 의존성 설치
COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# app 파일 복사
COPY ./src /usr/app/src
COPY ./local.sqlite /usr/app/local.sqlite

# env
ENV FLASK_APP "src.app:create_app('local')"
ENV GAME_FILE_URL "/storage/files/game_file/"

# port
EXPOSE 5002

# 데이터 보존 volumes
VOLUME [ "/usr/app/src/files/game_file" ]

# CMD ["python", "app.py"]

# docker run
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5002"]
