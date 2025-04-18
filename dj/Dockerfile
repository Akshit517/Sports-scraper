

FROM python:3.10-slim

WORKDIR /app

COPY dj/ /app
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4001

CMD ["python", "manage.py", "runserver", "0.0.0.0:4001"]

