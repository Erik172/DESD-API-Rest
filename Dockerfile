FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN pip install -r requirements.txt

COPY . .

# RUN flask db init

# RUN flask db migrate

# RUN flask db upgrade

EXPOSE 5000

CMD ["python", "app.py"]