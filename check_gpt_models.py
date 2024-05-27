from _apps.gpt_app.gpt_connect.gpt_connect import available_models

models = available_models()
for model in models:
    print(f"\n{model['id']}")