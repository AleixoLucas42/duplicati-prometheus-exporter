#!/bin/python3

import os
from flask import Response, Flask, request, make_response, jsonify, abort
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Gauge
from classes.duplicati import Duplicati

app = Flask(__name__)

graphs = {}
graphs["duplicati_backup_ops"] = Counter(
    "duplicati_backup_ops",
    "The total number of backups done",
    ["operation_name", "backup_name", "result"],
)
graphs["begin_time"] = Gauge(
    "begin_time", "Begin Time", ["backup_name", "operation_name", "result"]
)
graphs["end_time"] = Gauge(
    "end_time", "End Time", ["backup_name", "operation_name", "result"]
)
graphs["duration"] = Gauge(
    "duration", "Duration", ["backup_name", "operation_name", "result"]
)
graphs["backup_list_count"] = Gauge(
    "backup_list_count",
    "Backup List Count",
    ["backup_name", "operation_name", "result"],
)
graphs["bytes_uploaded"] = Gauge(
    "bytes_uploaded", "Bytes Uploaded", ["backup_name", "operation_name", "result"]
)
graphs["bytes_downloaded"] = Gauge(
    "bytes_downloaded", "Bytes Downloaded", ["backup_name", "operation_name", "result"]
)
graphs["files_uploaded"] = Gauge(
    "files_uploaded", "Files Uploaded", ["backup_name", "operation_name", "result"]
)
graphs["files_downloaded"] = Gauge(
    "files_downloaded", "Files Downloaded", ["backup_name", "operation_name", "result"]
)
graphs["files_deleted"] = Gauge(
    "files_deleted", "Files Deleted", ["backup_name", "operation_name", "result"]
)
graphs["folders_created"] = Gauge(
    "folders_created", "Folders Created", ["backup_name", "operation_name", "result"]
)
graphs["free_quota_space"] = Gauge(
    "free_quota_space", "Free Quota Space", ["backup_name", "operation_name", "result"]
)
graphs["total_quota_space"] = Gauge(
    "total_quota_space",
    "Total Quota Space",
    ["backup_name", "operation_name", "result"],
)
graphs["is_last_backup_failed"] = Gauge(
    "is_last_backup_failed",
    "1 means last backup failed",
    ["backup_name", "operation_name"],
)


graphs["duplicati_backup_summary"] = Summary(
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
    graphs["duplicati_backup_ops"].labels(
        operation_name=backup.operation_name,
        backup_name=backup.backup_name,
        result=backup.result,
    ).inc()


def backup_summary(backup):
    graphs["duplicati_backup_summary"].labels(
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


def backup_gauge(backup):
    graphs["begin_time"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.begin_time)
    graphs["end_time"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.end_time)
    graphs["duration"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.duration)
    graphs["backup_list_count"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.backup_list_count)
    graphs["bytes_uploaded"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.bytes_uploaded)
    graphs["bytes_downloaded"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.bytes_downloaded)
    graphs["files_uploaded"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.files_uploaded)
    graphs["files_downloaded"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.files_downloaded)
    graphs["files_deleted"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.files_deleted)
    graphs["folders_created"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.folders_created)
    graphs["free_quota_space"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.free_quota_space)
    graphs["total_quota_space"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
        result=backup.result,
    ).set(backup.total_quota_space)

def is_last_backup_failed(backup):
    graphs["is_last_backup_failed"].labels(
        backup_name=backup.backup_name,
        operation_name=backup.operation_name,
    ).set(backup.is_last_backup_failed)

@app.route("/", methods=["POST"])
def post_backup():
    if request.is_json:
        data = request.json
        backup = Duplicati(data)
        print(
            f"[+] {backup.operation_name} for {backup.backup_name} was finished with {backup.result} status"
        )
        if backup.result is "Fail":
            print(f"[!] {backup.message}")
            is_last_backup_failed(backup)
        else:
            backup_summary(backup)
            backup_gauge(backup)
            is_last_backup_failed(backup)
        backup_inc(backup)
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


@app.route("/", methods=["GET"])
def get_backup():
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("DUPLICATI_EXPORTER_PORT", 5000))
