from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from your simple Python server! by Sangeetth Paul"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))  # 10000 is a fallback, but Render will set PORT automatically
    app.run(host="0.0.0.0", port=port)


