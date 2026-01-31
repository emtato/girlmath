# Description:
# Created by Emilia on 2026-01-31

import pathlib

from google import genai
from google.genai import types
from google.genai.types import HttpOptions, Part

client = genai.Client(api_key='key')
model_id = "gemini-2.5-flash"


filepath = pathlib.Path('syllabus.pdf')

prompt = "   "
response = client.models.generate_content(
  model="gemini-3-flash-preview",
  contents=[
      prompt
  ]
)
print(response.text)

#
# pdf_file = Part.from_uri(
#     file_uri="https://future.utoronto.ca/sites/default/files/assets/files/2025/UofT_UAB_2025-26_FINAL-pages-compressed.pdf",
#     mime_type="application/pdf",
# )
#
# response = client.models.generate_content(
#     model=model_id,
#     contents=[pdf_file, prompt],
# )
#
# print(response.text)
# # Example response:
# # Here is a summary of the document in 300 words.
# #
# # The paper introduces the Transformer, a novel neural network architecture for
# # sequence transduction tasks like machine translation. Unlike existing models that rely on recurrent or
# # convolutional layers, the Transformer is based entirely on attention mechanisms.
# # ...
