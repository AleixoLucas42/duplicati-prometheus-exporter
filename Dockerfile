FROM python:3.10.14-slim-bullseye

WORKDIR /app

COPY requirements.txt .
COPY ./duplicati-prometheus-exporter/ ./duplicati-prometheus-exporter

RUN ls -lah /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["duplicati-prometheus-exporter"]