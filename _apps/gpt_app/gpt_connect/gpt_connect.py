import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def available_models():
    models = openai.Model.list()
    for model in models['data']:
        print(model['id'])
    return models['data']


def get_gpt4_response(prompt, model="gpt-4o", temperature=0.7, max_tokens=150, **kwargs):
    role_system_content = "You are a helpful assistant." if not kwargs.get('role_system_content') else kwargs['role_system_content']
    print("!! PROMPT: ", prompt)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": role_system_content},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=15,
    )
    return response.choices[0].message['content'].strip()

def get_gpt4_response_updated(prompt, model="gpt-4", temperature=0.7, max_tokens=150, **kwargs):
    if not openai.api_key:
        logging.error("API key for OpenAI is not set.")
        raise ValueError("API key for OpenAI is not set.")

    # Определение системной роли
    incorrect_picture_status = "Невозможно восстановить текст."
    role_system_content = kwargs.get(
        'role_system_content',
        f"Это некорректно распознанный OCR чек из магазина. Восстанови его и пришли в формате: "
        f"штрих-код продукта; продукт; единица измерения; цена; количество; стоимость. "
        f"Каждый следующий продукт с новой строки. Ответь без лишнего текста, только по сути. "
        f"Если текст невозможно восстановить, выдай ответ: {incorrect_picture_status}"
    )

    logging.debug(f"!! PROMPT: {prompt}")
    logging.debug(f"!! ROLE_SYSTEM_CONTENT: {role_system_content}")

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": role_system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            timeout=15,
        )
        logging.debug(f"!! RESPONSE: {response}")
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        logging.error(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    available_models()
