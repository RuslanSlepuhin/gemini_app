import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from _apps.gemini_app.geminitrial.views import gemini_ai

app = Flask(__name__)
CORS(app)

@app.route("/gemini_request", methods=["POST"])
async def gemini_request():
    question = request.json['request']
    answer = await gemini_ai(question)
    return jsonify({'answer': answer})

app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)))
