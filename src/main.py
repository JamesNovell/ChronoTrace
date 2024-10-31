import json
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "logs.json")

handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=15
)
handler.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)
        
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)
logger.addHandler(handler)        
        
@app.post("/log")
async def receive_log(request: Request):
    log_data = await request.json()
    logger.info(json.dumps(log_data))
    return {"status": "Log received", "log_data": log_data}