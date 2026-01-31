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
#touch /opt/api/girlmath/use_case/__init__.py
#touch /opt/api/girlmath/api/__init__.py
#touch /opt/api/girlmath/ai/__init__.py

# python -m pip install -U pip
# python -m pip install "uvicorn[standard]"
# which uvicorn


"""  
       
curl -X POST "http://147.182.158.24:7000/save_journal_entry"\ 
  -H "Content-Type: application/json"\
  -d '{"title": "migu", "content":"hello journal!","date":1706668800,"user_ID":"1adsa2aaf3"}'

"""

#  curl -X POST "http://147.182.158.24:7000/save_journal_entry" -H "Content-Type: application/json" -d '{"title":"MIGUU","content":"hello MIGU!! :D","date":1706668800,"user_ID":"1adsa2aaf3"}'

#  curl -X POST "http://147.182.158.24:7000/save_questionnaire" -H "Content-Type: application/json" -d '{"quiz": {"questino1":6,"question2":7},"date":1706668800,"user_ID":"1adsa2aaf3", "yesterday_goal": 0, "tomorrow": "BYEEEE"}'

# curl "http://147.182.158.24:7000/get_journal?journal_id=697e5a6a0c2a9e69c3a41bc1"

# curl "http://147.182.158.24:7000/get_quiz?quiz_id=697e59de0c2a9e69c3a41bc0"

# curl "http://147.182.158.24:7000/get_all?user_ID=1adsa2aaf3"
