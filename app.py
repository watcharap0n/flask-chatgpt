"""
Create a Flask app for web application chatbot using engine openai
- Framework web application: Flask
- Framework frontend web application: Vue.js
- Storage data local a simple

Detail:
- Flask app: app.py
- Vue.js app: index.html using CDN
- Storage data: data.json
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

*make api for chatbot from example above

APIs:
- GET / return index.html
- GET /get-data return data.json
- POST /chatbot payload: {message: 'Hello!'} return {message: 'Answer', role: 'system'}

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
        json.dump([], f)


# Route index
@app.route("/")
def index():
    return render_template("index.html")

# Route to get data from json
@app.route("/get-data")
def get_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


# Route chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():

    # Get data from frontend
    data = request.get_json()
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
    answer = data_response['choices'][-1]['message']['content']
    
    # Get data from data.json
    with open("data.json", "r") as f:
        data = json.load(f)

    data.append({"question": question, "answer": answer})

    # Save data to data.json
    with(open("data.json", "w")) as f:
        json.dump(data, f)

    return jsonify({'answer': answer})



# Run app
if __name__ == "__main__":
    app.run(debug=True)
