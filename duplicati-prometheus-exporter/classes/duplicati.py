#!/bin/python3
from datetime import datetime
import pytz


class Duplicati:
    def __init__(self, result):
        has_stack_trace = "StackTraceString" in result.get("Data")
        has_class_name = "ClassName" in result.get("Data")
        has_exception = result.get("Exception") != "None"

        if has_stack_trace or has_class_name or has_exception:
            self.result = "Fail"
            if has_exception:
                self.message = result.get("Exception")
            else:
                self.message = result.get("Data")["Message"]
            self.backup_name = result.get("Extra")["backup-name"]
            self.operation_name = result.get("Extra")["OperationName"]
            self.is_last_backup_failed = 1
        else:
            self.is_last_backup_failed = 0
            self.operation_name = result.get("Extra")["OperationName"]
            self.backup_name = result.get("Extra")["backup-name"]
            self.result = result.get("Data")["ParsedResult"]
            self.begin_time = self.convert_epoch(result.get("Data")["BeginTime"])
            self.end_time = self.convert_epoch(result.get("Data")["EndTime"])
            self.duration = self.convert_duration(
                self.rm_spaces(result.get("Data")["Duration"])
            )
            self.backup_list_count = result.get("Data")["BackendStatistics"][
                "BackupListCount"
            ]
            self.bytes_uploaded = result.get("Data")["BackendStatistics"][
                "BytesUploaded"
            ]
            self.bytes_downloaded = result.get("Data")["BackendStatistics"][
                "BytesDownloaded"
            ]
            self.files_uploaded = result.get("Data")["BackendStatistics"][
                "FilesUploaded"
            ]
            self.files_downloaded = result.get("Data")["BackendStatistics"][
                "FilesDownloaded"
            ]
            self.files_deleted = result.get("Data")["BackendStatistics"]["FilesDeleted"]
            self.folders_created = result.get("Data")["BackendStatistics"][
                "FoldersCreated"
            ]
            self.total_quota_space = result.get("Data")["BackendStatistics"][
                "TotalQuotaSpace"
            ]
            self.free_quota_space = result.get("Data")["BackendStatistics"][
                "FreeQuotaSpace"
            ]

    def convert_epoch(self, date):
        new_date = self.rm_spaces(date)
        date_object = datetime.strptime(new_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_object = date_object.replace(tzinfo=pytz.UTC)
        return date_object.timestamp()

    def rm_spaces(self, string):
        return string.replace(" ", "")

    def convert_duration(self, duration_str):
        h, m, s = duration_str.split(":")
        s, ms = s.split(".")

        total_seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1_000_000
        return total_seconds
