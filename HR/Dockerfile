FROM python:3.8.5

WORKDIR usr/src/HR

ENV PYTHONDONWRITBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .