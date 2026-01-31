# Description: main file running on digitalocean web server
# Created by Emilia on 2026-01-31
from fastapi import FastAPI
from use_case.save_quiz import save_quiz
app = FastAPI()

@app.post("/save_questionnaire")
def receive(data: dict):
    save_quiz(data)
    return{
        "response": "success"
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

