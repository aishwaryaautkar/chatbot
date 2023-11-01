from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as palm

app = Flask(__name__)

def set_api_key():
    try:
        load_dotenv()
        api_key = os.getenv('PALMAI_API_KEY')
        palm.configure(api_key=api_key)
    except Exception as e:
        print(f"An error occurred while setting the API key: {e}")

def get_palm_response(user_prompt):
    try:
        model = "models/text-bison-001"
        prompt = f"You are a healthcare chatbot and you have the ability to give home remedies for {user_prompt}."

        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=800,
        )

        return completion.result
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    palm_response = get_palm_response(msg)
    return palm_response

if __name__ == '__main__':
    set_api_key()
    app.debug = True
    app.run()





