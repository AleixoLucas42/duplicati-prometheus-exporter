#!/bin/python3

from flask import Response, Flask, request, make_response, jsonify
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from classes import duplicati

app = Flask(__name__)

graphs = {}
graphs['c'] = Counter('duplicati_backup_ops_total', 'The total number of backups done')


@app.route('/backup', methods=['POST'])
def get_backup():
    if request.is_json:
        data = request.json
        result = duplicati.Duplicati(data)
        print(result.result)
        response = make_response(jsonify({"message": "received"}), 204)
    else:
        response = make_response(jsonify({"message": "Check if your duplicati 'send-http-result-output-format' is set to json"}), 400)

    return response

@app.route("/")
def hello():
    graphs['c'].inc()
    
    return "Hello World!"

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)