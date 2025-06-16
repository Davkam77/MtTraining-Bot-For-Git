import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_openai(question: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        temperature=0.7
    )
    return response.choices[0].message["content"]
