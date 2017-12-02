#
# Dockerfile to build production hacarus-api-v2 image
#
# docker build -t hacarus-api-v2 .
# docker run --rm -v /opt/local/app/config:/opt/local/app/config hacarus-api-v2 -c config/production.json -r 0
#
FROM python:3.6.0
MAINTAINER Takashi Someda <takashi@hacarus.com>

# Download swig
RUN wget http://downloads.sourceforge.net/swig/swig-3.0.5.tar.gz && \
    tar -xvzf swig-3.0.5.tar.gz && cd swig-3.0.5 && \
    ./configure --prefix=/usr && make && make install && cd .. && \
    rm -Rf swig-3.0.5 && rm swig-3.0.5.tar.gz
# Swig dependencies
RUN apt-get update && apt-get install -y libpulse-dev --no-install-recommends

RUN pip install --upgrade pip

RUN mkdir -p /opt/local/app
WORKDIR /opt/local/app

COPY requirements.lock .
ARG PIP_EXTRA_INDEX_URL
RUN pip install -r requirements.lock
COPY run.py run.py
COPY tests tests
COPY app app

EXPOSE 3000
ENTRYPOINT ["python", "run.py"]
