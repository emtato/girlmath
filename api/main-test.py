# Description: main file running on digitalocean web server
# Created by Emilia on 2026-01-31
from fastapi import FastAPI

app = FastAPI()

@app.post("/save_questionnaire")
def receive(data: dict):
    text = data["message"]
    return {
        "reply": f"Backend received: {text}"
    }


@app.post("/save_journal_entry")
def receive(data: dict):
    text = data["message"]
    return {
        "reply": f"Backend received: {text}"
    }


@app.post("/ai_request")
def receive(data: dict):
    text = data["message"]
    return {
        "reply": f"Backend received: {text}"
    }

