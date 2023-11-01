"""
Create a Flask app for web application chatbot using engine openai
- Framework web application: Flask
- Framework frontend web application: Vue.js
- Framework chatbot: OpenAI
- Storage data local a simple

Detail:
- Flask app: app.py
- Vue.js app: index.html using CDN
- Create a function for generate response from OpenAI model: generate_response(prompt, model_engine)
- Create a function for API routes: chatbot(), get_data()
- Save data "question" and "answer": history.json 
- Save "message" from user and chatbot: data.json

history.json (example):
[{'question': 'Hello', 'answer': 'Hi'}]

data.json:
[{'role': 'user', 'content': 'Hello!'}] 

APIs:
- GET "/" return index.html
- GET "/get-data" return history.json
- POST "/chatbot payload" {message: 'Hello!'} return {answer: 'Answer from model'}

Example for call model "gpt-3.5-turbo":
    >>> openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages # import from data.json
        )

Author: Watcharapon Weeraborirak
"""

# app.py
from flask import Flask, request, jsonify, render_template
import openai
import json
import os

app = Flask(__name__)

# Set Environment API Key
openai.api_key = os.environ.get('OPENAI_API_KEY')

if not os.path.exists('history.json'):
    with open('history.json', 'w') as f:
        f.write('[]')

if not os.path.exists('data.json'):
    with open('data.json', 'w') as f:
        f.write('[]')

# Load history and data
with open('history.json', 'r') as f:
    history = json.load(f)
with open('data.json', 'r') as f:
    data = json.load(f)

def generate_response(prompt, model_engine="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=prompt
    )
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(history)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json['message']

    # Save message from user
    data.append({'role': 'user', 'content': message})

    response = generate_response(data)

    # get answer from model
    answer = response.choices[-1]['message']['content']

    # Save answer from model
    history.append({'question': message, 'answer': answer})


    # Dump data to json file
    with open('history.json', 'w') as f:
        json.dump(history, f)
    
    # Dump history to json file
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True)