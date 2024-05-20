#!/bin/python3

class Duplicati:
    def __init__(self, result):
        self.operation_name = result.get('Extra')['OperationName']
        self.backup_name = result.get('Extra')['backup-name']
        self.result = result.get('Data')['ParsedResult']
        self.begin_time = result.get('Data')["BeginTime"]
        self.end_time = result.get('Data')["EndTime"]
        self.diration = result.get('Data')["Duration"]