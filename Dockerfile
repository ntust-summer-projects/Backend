FROM python:3.11

RUN mkdir /code
WORKDIR /code
COPY linux_requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r linux_requirements.txt
