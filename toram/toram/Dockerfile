FROM python:3.9.10
ENV PYTHONUNBUFFERED 1

WORKDIR /toram-lobi
COPY requirements.txt /toram-lobi/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /toram-lobi/

