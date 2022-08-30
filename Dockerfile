FROM ubuntu:20.04

WORKDIR /home/api

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -yq \
    python3.8 \
    python3-distutils \
    python3-pip

COPY . .

RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--reload"]
