#!/bin/bash

APP="anusr-website"

docker build -t ${APP} .

docker run -d -p 80:80 anusr-website

echo ${APP}
