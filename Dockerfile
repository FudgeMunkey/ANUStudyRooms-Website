FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip3 install flask requests

# Set the Date/Time of the machine
RUN ln -fs /usr/share/zoneinfo/Australia/Sydney > /etc/localtime
RUN apt-get install -y tzdata
RUN echo "Australia/Sydney" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN mkdir Website
WORKDIR Website
COPY ./ ./

EXPOSE 80

CMD ["python3", "app.py"]

