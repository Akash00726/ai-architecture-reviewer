import os
from dotenv import load_dotenv
from .config import load_config

load_dotenv()

config = load_config()

PROVIDER = config["ai"]["provider"].lower()
MODEL = config["ai"]["model"]
TEMPERATURE = config["ai"].get("temperature", 0.2)


def generate_review(prompt):

    if PROVIDER == "gemini":
        return generate_with_gemini(prompt)

    return generate_with_openai(prompt)


# ---------- OPENAI ----------

def generate_with_openai(prompt):

    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": """
You are a senior cloud security architect.

Respond EXACTLY in this format:

Risk Score: LOW | MEDIUM | HIGH | CRITICAL

Findings:
- finding 1
- finding 2

Recommendations:
- recommendation 1
- recommendation 2
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=TEMPERATURE,
        max_tokens=800
    )

    return response.choices[0].message.content


# ---------- GEMINI ----------

def generate_with_gemini(prompt):

    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel(MODEL)

    full_prompt = f"""
You are a senior cloud security architect.

Respond EXACTLY in this format:

Risk Score: LOW | MEDIUM | HIGH | CRITICAL

Findings:
- finding 1
- finding 2

Recommendations:
- recommendation 1
- recommendation 2

Architecture:
{prompt}
"""

    response = model.generate_content(full_prompt)

    return response.text