FROM python:alpine

WORKDIR /usr/src/app

COPY tools/.pg_service.conf /root/.pg_service.conf

RUN pip install --upgrade pip && pip install django psycopg[binary]

EXPOSE 8000
EXPOSE 5432

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
