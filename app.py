"""
Create a Flask app for web application chatbot using engine openai
- Framework model chatbot module: openai
- Framework web application: Flask
- Framework frontend web application: Vue.js
- Storage data local a simple

Detail:
- Flask app: app.py
- Vue.js app: index.html using CDN
- Storage data: data.json
- Engine chatbot: openai (gpt-3.5-turbo) like a api POST https://api.openai.com/v1/chat/completions
- Fetch to this api https://api.openai.com/v1/chat/completions condition is Qestion and Answer for chatbot

Example:
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant." # Answer
      },
      {
        "role": "user",
        "content": "Hello!" # Question
      }
    ]
  }'

*make api for create chatbot from above example api

Author: Watcharapon Weeraborirak
"""

# Import library
import os
import json
import openai
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Create Flask app
app = Flask(__name__)

# Set key openai
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")

# Set environment
load_dotenv()


# Message is undefined it error frontend
if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({}, f)



# Route index
@app.route("/")
def index():
    return render_template("index.html")

# Route get data
@app.route("/get-data", methods=["GET"])
def get_data():
    # Get data from json file
    with open("data.json", "r") as f:
        data = json.load(f)

    # Return data to frontend
    return jsonify(data)

# Route chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    # Get data from frontend
    data = request.get_json()

    # Get data from json file
    with open("data.json", "r") as f:
        data_json = json.load(f)

    # Get question from frontend
    question = data["message"]

    # Set data for openai api
    data_openai = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    }

    # Set header for openai api
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
    }

    # Send request to openai api
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data_openai),
    )

    # Get data from openai api
    data_response = response.json()
    # Get answer from openai api
    answer = data_response['choices'][-1]['message']['content']
    # Return data to frontend
    return jsonify({'message': answer, 'role': 'system'})



# Run app
if __name__ == "__main__":
    app.run(debug=True)
