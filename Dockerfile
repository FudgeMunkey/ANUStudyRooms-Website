FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip3 install flask

RUN mkdir Website
WORKDIR Website
COPY ./ ./

EXPOSE 80

CMD ["python3", "app.py"]

