#!/bin/bash

APP="anusr-website-image"

docker build -t ${APP} .

docker-compose up
