import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini - UPDATED TO CURRENT API
gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
if not gemini_key or not gemini_key.startswith("AIza"):
    raise ValueError("Invalid or missing GEMINI_API_KEY")

genai.configure(api_key=gemini_key)

# Initialize model - LATEST VERSION
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Most current stable model


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400, headers

        # PROPER GENERATION CONFIG
        response = model.generate_content(
            user_message,
            generation_config={
                "max_output_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9
            },
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"
            }
        )

        return jsonify({"reply": response.text}), 200, headers

    except Exception as e:
        return jsonify({"error": str(e)}), 500, headers


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)