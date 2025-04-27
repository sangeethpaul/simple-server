import openai
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Get the OpenAI API key from environment variable (better practice)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send the user's message to OpenAI's GPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the reply from OpenAI's response
        bot_reply = response['choices'][0]['message']['content']

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
