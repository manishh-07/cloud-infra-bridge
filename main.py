from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from middleware import logging_middleware

load_dotenv()

app = FastAPI()

# Register structured logging middleware
app.middleware("http")(logging_middleware)

@app.get("/")
async def root_msg():
    return {"message": f"HELLO {os.getenv('APP_NAME')}"}

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/check-db-conn")
async def check_db_conn():
    if os.getenv("DB_ENABLED") == "False":
        raise HTTPException(
            status_code=500, detail="Database connection failed..!"
        )
    return {"status": "DB ENABLED"}