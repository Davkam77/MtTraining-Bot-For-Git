import openai
import os


async def ask_openai(prompt):
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        max_tokens=60,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
