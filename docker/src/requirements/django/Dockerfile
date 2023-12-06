FROM python:alpine

WORKDIR /usr/src/app

COPY tools/script.sh /

RUN pip install --upgrade pip && pip install django psycopg[binary]

EXPOSE 8000

ENTRYPOINT ["/script.sh"]
