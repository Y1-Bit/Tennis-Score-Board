FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
COPY app ./app
# COPY uwsgi.ini ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "--http", ":8000", "--wsgi-file", "app/wsgi.py"]
