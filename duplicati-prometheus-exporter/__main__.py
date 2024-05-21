#!/bin/python3

import os
from flask import Response, Flask, request, make_response, jsonify
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter
from classes.duplicati import Duplicati

app = Flask(__name__)

graphs = {}
graphs["c"] = Counter(
    "duplicati_backup_ops",
    "The total number of backups done",
    ["operation_name", "backup_name", "result"],
)
graphs["s"] = Summary(
    "duplicati_backup_summary",
    "Summary of duplicati backup jobs",
    [
        "backup_name",
        "result",
        "begin_time",
        "end_time",
        "duration",
        "bytes_uploaded",
        "bytes_downloaded",
        "files_uploaded",
        "files_downloaded",
        "files_deleted",
        "folders_created",
        "total_quota_space",
        "free_quota_space",
        "backup_list_count",
    ],
)


def backup_inc(backup):
    graphs["c"].labels(
        operation_name=backup.operation_name,
        backup_name=backup.backup_name,
        result=backup.result,
    ).inc()


def backup_summary(backup):
    graphs["s"].labels(
        backup_name=backup.backup_name,
        result=backup.result,
        begin_time=backup.begin_time,
        end_time=backup.end_time,
        duration=backup.duration,
        bytes_uploaded=backup.bytes_uploaded,
        bytes_downloaded=backup.bytes_downloaded,
        files_uploaded=backup.files_uploaded,
        files_downloaded=backup.files_downloaded,
        files_deleted=backup.files_deleted,
        folders_created=backup.folders_created,
        total_quota_space=backup.total_quota_space,
        free_quota_space=backup.free_quota_space,
        backup_list_count=backup.backup_list_count,
    ).observe(1)


@app.route("/", methods=["POST"])
def get_backup():
    if request.is_json:
        data = request.json
        backup = Duplicati(data)
        backup_inc(backup)
        backup_summary(backup)
        print(f"[+] {backup.operation_name} for {backup.backup_name} was finished with {backup.result} status")
        response = make_response(jsonify({"message": "Received"}), 204)
    else:
        response = make_response(
            jsonify(
                {
                    "message": "Check if your duplicati 'send-http-result-output-format' is set to json"
                }
            ),
            400,
        )

    return response


@app.route("/metrics")
def requests_count():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("DUPLICATI_EXPORTER_PORT", 5000))
