FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    netcat-openbsd

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install psycopg2

COPY . .

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "wsgi:app"]
CMD [ "python", "wsgi.py" ]