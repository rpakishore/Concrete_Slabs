# app/Dockerfile
# MUltistage build
# First Image
FROM python:3.10-slim AS compile-image

WORKDIR /app

ENV FLIT_ROOT_INSTALL=1
ARG PIP_DISABLE_PIP_VERSION_CHECK=1
ARG PIP_NO_CACHE_DIR=1

RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common
RUN rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install --no-cache-dir --upgrade pip

COPY requirements.txt ./requirements.txt

RUN pip3 install --no-cache -r requirements.txt

FROM python:3.10-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
WORKDIR /app

RUN mv /app/.streamlit ~/.streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "About.py", "--server.port=8501", "--server.address=0.0.0.0"]
