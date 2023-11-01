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
- GET "/get-data" return data.json
- POST "/chatbot payload" {message: 'Hello!'} return {answer: 'Answer from model'}

Example for call model "gpt-3.5-turbo":
    >>> openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages # import from data.json
        )

Author: Watcharapon Weeraborirak
"""