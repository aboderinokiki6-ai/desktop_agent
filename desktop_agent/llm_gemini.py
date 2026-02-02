from __future__ import annotations
import os, json
import google.generativeai as genai

SYSTEM = """You are a desktop automation agent.
You must return ONLY valid JSON. No markdown.

Task: classify and propose an action for a file in Downloads.

You can choose one action:
- {"action":"move","category":"Documents|Pictures|Videos|Audio|Archives|Installers|Code|Other","new_name":"...","reason":"..."}
- {"action":"skip","reason":"..."}

Rules:
- new_name must keep original extension.
- prefer clean human names (no "finalfinal", no random numbers).
- if file type is unknown or risky, choose skip.
"""

def model():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable.")
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-1.5-flash")

def classify_file(file_info: dict) -> dict:
    prompt = SYSTEM + "\n\nINPUT:\n" + json.dumps(file_info, ensure_ascii=False)
    resp = model().generate_content(prompt)
    text = resp.text.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(text)
