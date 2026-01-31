# Description:
# Created by Emilia on 2026-01-31
from fastapi import FastAPI

app = FastAPI()

@app.post("/send") #if frontend sends info,run this
def receive(data: dict): #automatically parse incoming json to dickt
    text = data["message"]
    return {
        "reply": f"Backend received: {text}" # return info in dict format (converted automatically to json)
    }


# run fastapi sever
# /opt/api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
# scp -r /Users/emtato/PycharmProjects/girlmath root@147.182.158.24:/opt/api

"""
scp -r project_root \
    --exclude venv \
    --exclude .venv \
    --exclude .git \
    --exclude __pycache__ \
    root@147.182.158.24:/opt/api
    """
