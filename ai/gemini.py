# Description:
# Created by Emilia on 2026-01-31

import pathlib

from google import genai
from google.genai import types
from google.genai.types import HttpOptions, Part

from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
model_id = "gemini-2.5-flash"

filepath = pathlib.Path('syllabus.pdf')

prompt = "   "

# response = client.models.generate_content(
#   model="gemini-3-flash-preview",
#   contents=[
#       prompt
#   ]
# )
# print(response.text)
