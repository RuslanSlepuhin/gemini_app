from _apps.gemini_app.geminitrial.models import model


async def gemini_ai(prompt):
    prompt = prompt
    response = model.generate_content(contents=[prompt])
    print(f"\033[1;33m{response}\033[0m")
    return response.text
