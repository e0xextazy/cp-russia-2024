import sys
import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": datetime.now().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_record, ensure_ascii=False)


json_formatter = JSONFormatter()

file_handler = logging.FileHandler("api.log.jsonl")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(json_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
