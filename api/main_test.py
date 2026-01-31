# Description: main file running on digitalocean web server
# Created by Emilia on 2026-01-31
from fastapi import FastAPI, HTTPException

from ai.gemini import prompt
from use_case.retrieve_quiz import retrieve_quiz_by_id
from use_case.retrieve_quizzes_journals import retrieve_all_quizzes_and_journals
from use_case.save_journal import save_journal
from use_case.save_quiz import save_quiz
from use_case.prompt_ai import prompt_ai
from use_case.prompt_ai import convert_ai
from use_case.retrieve_journal import retrieve_journal_by_id

app = FastAPI()
# test
@app.post("/save_questionnaire")
def receive(data: dict):
    try:
        save_quiz(data)
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save_journal_entry")
def receive(data: dict):
    try:
        save_journal(data)
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ai_request")
def receive(data: dict):
    try:
        newData = convert_ai(data)
        prompt_ai(newData)
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_quiz")
def receive(quiz_id: str):
    try:
        retrieve_quiz_by_id(quiz_id)
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_journal")
def receive(journal_id: str):
    try:
        retrieve_journal_by_id(journal_id)
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_all")
def receive():
    try:
        retrieve_all_quizzes_and_journals()
        return {"response": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





