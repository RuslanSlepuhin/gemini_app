from geminitrial.models import model


def gemini_ai(prompt):
    prompt = prompt
    response = model.generate_content(contents=[prompt])
    return response.text
