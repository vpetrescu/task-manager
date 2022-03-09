FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
USER root

# Install Python dependencies
RUN apt-get update

RUN apt install -y  \
    python3.9  \
    python3-setuptools \
    python3-pip

RUN pip3 install pytest

ARG python_src=""

ENV WORK_DIR /opt/build
ENV PYTHONPATH "${WORK_DIR}/python"

RUN mkdir -p ${PYTHONPATH}

COPY ${python_src} ${PYTHONPATH}

RUN python3 /opt/build/python/setup.py install
