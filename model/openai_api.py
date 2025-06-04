from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL, TEMPERATURE

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_openai(prompt: str, model=DEFAULT_MODEL) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)