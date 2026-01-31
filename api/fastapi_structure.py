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
