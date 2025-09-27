from google import genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Only load .env if not running in production
if os.environ.get("ENV", "dev").lower() != "prod":
    load_dotenv()

class Skill(BaseModel):
    skill: str

client = genai.Client()

model_order = [
    'gemini-2.5-flash-lite',
    'gemini-2.0-flash-lite',
]

def fix_skill_names(skills):
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model_order[attempt],
                contents=(
                    "Make the following skills more formal and professional, suitable for a resume. "
                    "For each skill, change it to a broader skill or expand any abbreviation to its full name. "
                    "**IMPORTANT NOTE**: YOU ALWAYS NEED TO RETURN IN CORRECT ORDER.\nSkills: " + str(skills)
                ),
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[Skill],
                },
            )
            return [s.skill for s in response.parsed]
        except Exception:
            if attempt == max_retries:
                return skills

if __name__ == "__main__":
    skills = ["M2M", "NLP", "PyTorch"]
    response = fix_skill_names(skills)
    print(response)