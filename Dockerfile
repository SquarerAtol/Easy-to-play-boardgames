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

# Copy requirements and install dependencies
COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY ./src /usr/app/src
COPY ./local.sqlite /usr/app/local.sqlite

# env
ENV FLASK_APP "src.app:create_app('local')"
ENV GAME_FILE_URL "/storage/files/game_file/"

# port
EXPOSE 5002

# Volumes for data persistence
VOLUME [ "/usr/app/src/files/game_file" ]

# docker run
# CMD ["flask", "run", "-h", "0.0.0.0"]

# Start the application using Gunicorn
RUN pip install gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5002", "src.app:create_app('local')"]
