import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# Safe API key loading
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("No GEMINI_API_KEY found in environment variables")

# Configure with explicit settings
genai.configure(
    api_key=gemini_key,
    transport="rest",  # Avoids gRPC issues
    client_options={
        "api_endpoint": "generativelanguage.googleapis.com"
    }
)


@app.route("/chat", methods=["POST"])
def chat():
    # Add CORS headers if needed
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    try:
        response = model.generate_content(
            request.json["message"],
            generation_config={"max_output_tokens": 150}
        )
        return jsonify({"reply": response.text}), 200, headers
    except Exception as e:
        return jsonify({"error": str(e)}), 500, headers

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Gemini API call
        response = model.generate_content(
            user_message,
            generation_config={
                "max_output_tokens": 150,
                "temperature": 0.7
            }
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)