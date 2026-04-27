from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import traceback

app = Flask(__name__)

# --- CONFIGURATION ---
# Make sure GROQ_API_KEY is set in your Render Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Global memory (Note: Resets when Render server sleeps)
conversation_history = []

# --- SYSTEM PROMPT (The Personality) ---
PA_PERSONALITY = (
    "You are J.A.R.V.I.S., Ridhu's advanced ECE Personal Assistant. "
    "1. Language: You are bilingual. Speak and understand English, Tamil, and Tanglish fluently. "
    "2. Concise Rule: Keep replies under 2 sentences unless Ridhu asks for a deep dive, brainstorm, or a game. "
    "3. Expertise: You are a genius in VLSI, RISC-V, and 6G SoC design. "
    "4. Tone: Witty, professional, and futuristic. Address him as Ridhu."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    try:
        data = request.json
        user_input = data.get("message")
        
        # 1. Prepare history (Keep last 10 exchanges for memory)
        messages = [{"role": "system", "content": PA_PERSONALITY}]
        messages.extend(conversation_history[-10:])
        messages.append({"role": "user", "content": user_input})

        # 2. Call the powerful Llama 3.3 70B model
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        
        reply = completion.choices[0].message.content
        
        # 3. Update history
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})

    except Exception as e:
        print("--- SERVER CRASH LOG ---")
        traceback.print_exc()
        return jsonify({"reply": "Sorry Ridhu, my memory circuits glitched. Check the logs."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
