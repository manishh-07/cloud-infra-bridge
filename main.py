from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root_msg():
    return f"HELLO {os.getenv('APP_NAME')}"

@app.get("/health")
async def health():
    return {"status": "OK"}