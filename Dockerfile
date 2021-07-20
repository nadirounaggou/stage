FROM ubuntu:latest
COPY python_dir WORKDIR
RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install python3-mysql.connector -y
