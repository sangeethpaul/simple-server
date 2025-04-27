import openai
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set in your environment


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
        # Make the API call to OpenAI using the new method for chat-based interactions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # Set system instructions (if any)
                {"role": "user", "content": user_message}  # User's message
            ],
            max_tokens=150  # Limit the length of the response
        )

        # Extract the assistant's reply from the response
        bot_reply = response['choices'][0]['message']['content'].strip()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
