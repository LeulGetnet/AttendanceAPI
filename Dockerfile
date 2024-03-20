FROM python:3.6.13-alpine3.12


COPY requirements.txt /app/requirements.txt

RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ADD . .

EXPOSE 8000

CMD ["gunicorn", "--blind", ":8000", "--workers", "3", "attendanceSystem.wsgi:application"]


