FROM python:3.10-slim-buster

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

USER app

CMD ["python", "app/app.py"]

