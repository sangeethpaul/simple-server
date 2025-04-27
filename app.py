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
        # Use the new API call for chat models (openai.Completion.create())
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            prompt=user_message,  # Use the user input as a prompt
            max_tokens=150  # Limit the number of tokens in the response
        )

        # Extract the reply from OpenAI's response
        bot_reply = response['choices'][0]['text'].strip()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
