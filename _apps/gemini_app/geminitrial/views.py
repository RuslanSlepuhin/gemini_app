from _apps.gemini_app.geminitrial.models import model


async def gemini_ai(prompt):
    prompt = prompt
    try:
        response = model.generate_content(contents=[prompt])
        return response.text
    except Exception as ex:
        print(f"\033[1;33m{ex}\033[0m")
