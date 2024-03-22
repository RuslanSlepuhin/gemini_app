from _apps.gemini_app.geminitrial.models import model


async def gemini_ai(prompt):
    prompt = prompt
    response = model.generate_content(contents=[prompt])
    return response.text
