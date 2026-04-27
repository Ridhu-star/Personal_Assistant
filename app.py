from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace with your actual Groq Key
client = Groq(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are Ridhu's friendly ECE assistant and mentor. Be supportive and explain engineering concepts simply. Address him as Ridhu. Do not use markdown like asterisks or hashtags."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Sorry Ridhu, I had a connection glitch."}), 500

if __name__ == "__main__":
    # Port 5000 is standard for local; cloud hosts will override this
    app.run(host='0.0.0.0', port=5000)