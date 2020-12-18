FROM python:3.7.8-alpine

WORKDIR /usr/src/app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add gettext bash

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]