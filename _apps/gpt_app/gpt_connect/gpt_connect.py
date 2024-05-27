import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key


def available_models():
    models = openai.Model.list()
    for model in models['data']:
        print(model['id'])
    return models['data']


def get_gpt4_response(prompt, model="gpt-4o", temperature=0.7, max_tokens=150):
    print("!! PROMPT: ", prompt)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=15,
    )
    return response.choices[0].message['content'].strip()


if __name__ == "__main__":
    available_models()