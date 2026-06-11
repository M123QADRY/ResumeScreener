from google import genai
from pypdf import PdfReader
import json

# =====================================
# GEMINI API KEY
# =====================================

from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# =====================================
# READ RESUME PDF
# =====================================

reader = PdfReader("resume.pdf")

resume = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        resume += text + "\n"

# =====================================
# READ JOB DESCRIPTION
# =====================================

with open("job.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

# =====================================
# PROMPT
# =====================================

prompt = f"""
You are a strict technical recruiter.

Rules:
- Do not assume skills that are not explicitly mentioned.
- Penalize missing requirements.
- Give realistic scores.
- A score above 90 should be reserved for near-perfect matches.
- A score between 70 and 85 indicates a good but imperfect fit.
- Return only valid JSON.

Resume:
{resume}

Job Description:
{job_description}

Return ONLY valid JSON.

{{
    "match_score": 0,
    "strengths": [],
    "missing_skills": [],
    "recommendation": "",
    "reasoning": ""
}}
"""

# =====================================
# GEMINI REQUEST
# =====================================

print("Sending request...")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("Response received!")

result = response.text

print(result[:200])
# =====================================
# CLEAN JSON RESPONSE
# =====================================

result = response.text

result = result.replace("```json", "")
result = result.replace("```", "")
result = result.strip()

# =====================================
# CONVERT TO PYTHON OBJECT
# =====================================

data = json.loads(result)
print("\n===== RAW RESPONSE =====\n")
print(result)

# =====================================
# SAVE RESULT
# =====================================

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

# =====================================
# DISPLAY RESULT
# =====================================

print("\n===== SCREENING RESULT =====\n")

print(json.dumps(data, indent=4))

print("\nSaved to result.json")
