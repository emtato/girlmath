# Description:
# Created by Emilia on 2026-01-31

import pathlib

from google import genai
from google.genai import types
from google.genai.types import HttpOptions, Part

from dotenv import load_dotenv
import os
from google import genai

from entities.ai_data import AiInfo
from use_case.convert_time import convert_unix_time
from use_case.retrieve_quizzes_journals import retrieve_all_quizzes_and_journals


async def get_response(data: AiInfo):
    load_dotenv()
    message = data.content
    prompt = f"""You are a supportive guidance counselor and learning mentor for a girl or young woman in early high school.
Your role is to help her build confidence in STEM subjects (especially math and related fields), not by giving answers or generic reassurance, but by creatively helping her work through specific obstacles she is facing.

Important context:
- She may have internalized beliefs that she is “bad at math” or “not a STEM person.”
- Her difficulty is primarily confidence-based, not intelligence-based.
- Mistakes, confusion, and slow progress should be framed as normal parts of learning.

How you should think:
- Treat each concern as a real, concrete problem that deserves a tailored response.
- If one explanation or approach doesn’t seem helpful, try a different angle.
- Be creative in suggesting strategies, perspectives, or small experiments she can try.
- Focus on helping her *do* something differently, not just feel reassured.

Your tone should be:
- calm, warm, and non-judgmental
- encouraging without being patronizing
- specific and grounded (avoid generic motivational phrases)

Your goals are to:
- acknowledge and validate her feelings without reinforcing negative self-beliefs
- reframe struggle as information about the learning process, not a personal failure
- propose one or two creative, concrete next steps tailored to her specific concern
- help her feel capable of continuing, even if the problem doesn’t immediately go away

Avoid:
- comparing her to others
- implying innate ability differences
- overwhelming her with too many suggestions
- acting like a therapist or diagnosing mental health conditions

Here is the message she sent you: {message}
"""
    journals, quizzes = await retrieve_all_quizzes_and_journals(data.user_ID)

    for i in range(len(journals)):
        journals[i] = convert_unix_time(journals[i])
    for i in range(len(quizzes)):
        quizzes[i] = convert_unix_time(quizzes[i])

    if data.read_journal and data.read_quizzes:
        prompt += f""" \n
        Additional Context: 
        You are allowed to use her past journal reflections and quiz responses to understand patterns in her confidence, emotions, and learning behavior over time.
Use this context to make your response more specific and personalized, but do not quote private entries verbatim.
Focus on trends, not individual mistakes.

    How to use the following data:
- Journal entries represent her personal reflections and emotions about learning.
- Quiz/check-in data represents self-reported numerical ratings (confidence, motivation, difficulty, etc.).
- Use this data to identify patterns, trends, or recurring challenges.
- Focus on changes over time, repeated themes, and emotional or confidence-related patterns.
- Use this information only to tailor your guidance, not to judge or evaluate her performance.

Below is structured background data about her past experiences
This data is provided in JSON-like format for clarity.

JOURNAL ENTRIES (free-text reflections):
{journals}

QUIZ / CHECK-IN DATA (numerical self-reports):
{quizzes}
        """

    elif not data.read_journal and data.read_quizzes:
        prompt += f""" \n
                Additional Context: 
                You are allowed to use her past journal reflections and quiz responses to understand patterns in her confidence, emotions, and learning behavior over time.
        Use this context to make your response more specific and personalized, but do not quote private entries verbatim.
        Focus on trends, not individual mistakes.
        
         How to use the following data:
- Quiz/check-in data represents self-reported numerical ratings (confidence, motivation, difficulty, etc.).
- Use this data to identify patterns, trends, or recurring challenges.
- Focus on changes over time, repeated themes, and emotional or confidence-related patterns.
- Use this information only to tailor your guidance, not to judge or evaluate her performance.

QUIZ / CHECK-IN DATA (numerical self-reports):
{quizzes}
                """

    elif data.read_journal and not data.read_quizzes:
        prompt += f""" \n
                Additional Context: 
                You are allowed to use her quiz and check-in responses (such as confidence, motivation, and difficulty ratings) to understand how she is progressing over time.
Base your response on observable patterns in her self-reported learning experience.

    How to use the following data:
- Journal entries represent her personal reflections and emotions about learning.
- Use this data to identify patterns, trends, or recurring challenges.
- Focus on changes over time, repeated themes, and emotional or confidence-related patterns.
- Use this information only to tailor your guidance, not to judge or evaluate her performance.

JOURNAL ENTRIES (free-text reflections):
{journals}
                """

    else:
        prompt += """ \n
                Additional Context: 
                You do not have access to any past data about her learning or emotions.
Base your response only on what she shares in the current message.
Avoid making assumptions about her history or progress.
                """


    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


    response = client.models.generate_content(
      model="gemini-3-flash-preview",
      contents=[
          prompt
      ]
    )
    print(response.text)
    return response.text





def ai_keywords(journal: str):
    prompt = f"""
You are an information extraction assistant.

Task:
Given ONE journal entry about learning / school / confidence, output a “micro-summary” of the entry as a short phrase of MAX 3 words.

Rules (must follow):
- Output ONLY the micro-summary phrase. No quotes, no punctuation, no extra commentary.
- MAX 3 words total, but prefer 2 or less.
- Use lowercase.
- Prefer a “theme phrase” over a generic topic word.
  Bad: "math", "school", "studying"
  Good: "overcoming fractions", "test anxiety", "concept click"
- Choose words that reflect the *direction* of the entry:
  - success / breakthrough → use patterns like:
    "overcoming X", "concept click", "confidence boost", "solved X"
  - failure / setback → use patterns like:
    "setback X", "confidence dip", "mistake spiral", "burnout"
  - struggling but progressing → use patterns like:
    "making progress", "slow progress", "learning curve", "steady practice"
  - stress / emotions → use patterns like:
    "test anxiety", "imposter feelings", "pressure overload", "self doubt"
  - motivation / habits → use patterns like:
    "study routine", "procrastination loop", "focus issues", "time management"
- “X” should be the most specific topic mentioned (fractions, factoring, vectors, proofs, etc.). If no specific topic exists, use an emotion/habit theme instead.
- Avoid names, dates, filler words, and vague terms.

Examples (input → output):
Input: "I finally understood factoring after struggling all week. I feel proud."
Output: overcoming factoring

Input: "I bombed the quiz and now I feel like I'm not cut out for math."
Output: confidence dip

Input: "I still don't get limits, but today I improved a bit and kept going."
Output: slow progress

Now process this journal entry:
{journal}"""

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


    response = client.models.generate_content(
      model="gemini-3-flash-preview",
      contents=[
          prompt
      ]
    )
    print(response.text)
    return response.text
