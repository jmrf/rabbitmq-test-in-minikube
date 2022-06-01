FROM python:3.8-slim

RUN apt-get update -qq --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends \
    build-essential

RUN mkdir -p /app/data

WORKDIR /app

ARG PYPI_USR
ARG PYPI_PWD
ARG MAIPY_VERSION

RUN python -m pip install -U pip && \
    pip install --extra-index-url \
        https://"${PYPI_USR}":"${PYPI_PWD}"@pypi.melior.ai \
            maipy=="${MAIPY_VERSION}" && \
    pip list


COPY rabbit_test.py /app/rabbit_test.py

ENTRYPOINT ["python", "-m", "rabbit_test"]

