# Duplicati prometheus exporter
This is an simple exporter made for [Duplicati backup](https://duplicati.com).

## How it works
On your Duplicati backup interface or cli, you can configure in advanced options parameters for `"send-http"`, with this configuration, Duplicati will send an post request to this exporter; so then exporter will gather metrics receved and expose a /metrics for `prometheus`.

```bash
# Cli configuration example
--send-http-url=http://<duplicati-exporter-instance>:5000/
--send-http-result-output-format=Json
```

## Setup demo
For this demo is needed to be installed docker in your machine. How demo is setting up duplicati prometheus exporter app, prometheus and grafana, besides that, there is a configuration container that configure grafana datasource and dashboard, after that, this container send an example post to duplicati example exporter, you can see the configuration on [docker compose file](docker-compose.yml).
- In repository root, run:
> docker compose up --force-recreate
- After ~15 seconds the address `http://localhost:3000` should be ready. Go to [Grafana in your localhost](http://localhost:3000/d/ddmio2e27ctmod/duplicati-backup-dashboard)
> http://localhost:3000/d/ddmio2e27ctmod/duplicati-backup-dashboard

![Grafana dashboard example](docs/static/grafan-dash.png)
~This dashboard can change while i'm developing and improving.

## Run duplicati prometheus exporter using docker
Docker is the better way to execute this application. If you prefer, you can build your own
container image based on my [Dockerfile](Dockerfile) to change anythong you want and store your
container artifact where you need; but you also can use my docker image that is on my [dockerhub](https://hub.docker.com/repository/docker/aleixolucas/duplicati-prometheus-exporter/general)