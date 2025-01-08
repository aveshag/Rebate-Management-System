FROM ubuntu:latest
LABEL authors="avesh"

ENTRYPOINT ["top", "-b"]