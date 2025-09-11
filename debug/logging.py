# debug/logging.py

import os
import datetime

LOG_PATH = "logs/conversation.log"

class Logger:
    def __init__(self, log_path=LOG_PATH):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def write_log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message} \n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def clear_log(self):
        open(self.log_path, "w", encoding="utf-8").close()

    def read_log(self, last_n: int=10) -> str:
        with open(self.log_path,"r",encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-last+n:]) if lines else "(无记录)"