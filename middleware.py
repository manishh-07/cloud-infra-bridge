from datetime import datetime
from zoneinfo import ZoneInfo
import json
import logging
import time
import uuid
from fastapi import Request

# Setup standard logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("app")


async def logging_middleware(request: Request, call_next):
    start = time.time()
    req_id = str(uuid.uuid4())[:8]
    status_code = 500  # Default to 500 if unhandled error occurs

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        duration_ms = round((time.time() - start) * 1000, 2)
        is_success = status_code < 400

        # Current timestamp in IST (Indian Standard Time)
        ist_timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()

        log_data = {
            "timestamp": ist_timestamp,
            "level": "INFO" if is_success else "ERROR",
            "request_id": req_id,
            "method": request.method,
            "path": request.url.path,
            "status": status_code,
            "duration_ms": duration_ms,
            "outcome": "success" if is_success else "error",
        }

        if is_success:
            logger.info(json.dumps(log_data))
        else:
            logger.error(json.dumps(log_data))

# LOG LEVELS: INFO, ERROR, WARNING, DEBUG, 
# HTTP STATUS CODES: 
# 2xx -> ok
# 3xx -> redirection
# 4xx -> Backend error
# 5xx -> Infrastructure error
