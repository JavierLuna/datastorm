FROM python:3.6.6-alpine
MAINTAINER OrbitalAds "dev@orbitalads.io"

# Deploy app
RUN mkdir -p /usr/src/tests
ENV PYTHONPATH /usr/src/tests
WORKDIR /usr/src/tests
COPY . /usr/src/tests/

# install requirements
RUN python3 setup.py install
