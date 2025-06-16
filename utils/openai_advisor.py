from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем ключ и организацию из .env
api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORG_ID")      # Пример: org_ABCD123456
project = os.getenv("OPENAI_PROJECT_ID", None) # Необязательно

# Создаём клиента OpenAI
client = AsyncOpenAI(
    api_key=api_key,
    organization=organization,
    project=project
)

async def ask_openai(question: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты умный фитнес-советник. Отвечай кратко, полезно и дружелюбно."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Ошибка OpenAI: {e}"
