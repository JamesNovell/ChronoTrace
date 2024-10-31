import json
import logging
import yaml
import os
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

main_dir = os.path.join(os.path.dirname(__file__), "..")
config_path = os.path.join(main_dir, "config", "config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

log_dir = config['logging']['log_dir']
log_file = os.path.join(main_dir, log_dir, config['logging']['log_file'])
max_bytes = config['logging']['max_bytes']
backup_count = config['logging']['backup_count']
log_level = config['logging']['log_level']

os.makedirs(os.path.join(main_dir, log_dir), exist_ok=True)

handler = RotatingFileHandler(
    log_file, maxBytes=max_bytes, backupCount=backup_count
)
handler.setLevel(getattr(logging, log_level.upper()))

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)
        
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(getattr(logging, log_level.upper()))
app_logger.addHandler(handler)  
        
@app.post("/log")
async def receive_log(request: Request):
    log_data = await request.json()
    app_logger.info(json.dumps(log_data))
    return {"status": "Log received", "log_data": log_data}