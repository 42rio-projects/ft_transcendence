FROM python:alpine

WORKDIR /usr/src/app

COPY tools/script.sh ./
COPY tools/.pg_service.conf /root/.pg_service.conf

# RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5432

RUN ./script.sh

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
