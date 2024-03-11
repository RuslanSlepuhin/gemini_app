import os
from flask import Flask
from flask_cors import CORS
from flask import request
from geminitrial.views import gemini_ai

app = Flask(__name__)
CORS(app)

@app.route("/gemini_request", methods=["POST"])
def gemini_request():
    question = request.json['request']
    pass
    answer = gemini_ai(question)
    return {'answer': answer}

app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)))
