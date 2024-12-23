import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from _apps.gemini_app.geminitrial.views import gemini_ai
from _apps.gpt_app.gpt_connect.gpt_connect import get_gpt4_response, get_gpt4_response_updated

app = Flask(__name__)
CORS(app)

@app.route("/gemini_request", methods=["POST"])
async def gemini_request():
    question = request.json['request']
    answer = await gemini_ai(question)
    return jsonify({'answer': answer})

@app.route("/gpt_request", methods=["POST"])
async def gpt_request():
    question = request.json['request']
    tokens = request.json['tokens']
    answer = get_gpt4_response(question, max_tokens=tokens)
    return jsonify({'answer': answer})

@app.route("/gpt_request_updated", methods=["POST"])
async def gpt_request_updated():
    question = request.json['request']
    tokens = request.json['tokens']
    answer = get_gpt4_response_updated(question, max_tokens=tokens)
    return jsonify({'answer': answer})


app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)))
