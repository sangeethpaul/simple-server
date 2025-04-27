from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Load your OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Hello from your simple Python server! by Sangeetth Paul"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    user_message = data.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send the message to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract reply
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)
