from openai import OpenAI, OpenAIError
from app import app
from flask_babel import _

def translate(text, source_language, dest_language):
    if 'OPENAI_API_KEY' not in app.config or not app.config['OPENAI_API_KEY']:
        return _('Error: OPENAI_API_KEY is missing.')

    client = OpenAI(api_key=app.config['OPENAI_API_KEY'])

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who translates text."},
                {"role": "user", "content": f"Translate the following lyrics from {source_language} into {dest_language}:\n{text}"}
            ],
            temperature=0.5,
            top_p=1.0,
            max_tokens=2024,
            frequency_penalty=0,
            presence_penalty=0
        )
        if 'error' in response:
            print("Error occurred:", response.error.message)
        return response.choices[0].message.content.strip()

    except OpenAIError as e:
        print("An error occurred:", e)