from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import traceback  # Added for debugging

app = Flask(__name__)

# This looks for the key in Render Environment Variables
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message")
        
        # Log exactly what we are sending to Groq
        print(f"DEBUG: Ridhu said: {user_input}")
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Ridhu's friendly ECE assistant. Address him as Ridhu."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        # CRITICAL: This prints the EXACT error to your Render Logs
        print("--- DATABASE/API ERROR ---")
        traceback.print_exc() 
        return jsonify({"reply": "Sorry Ridhu, I had a connection glitch."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
