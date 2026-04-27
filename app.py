from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- MEMORY CONFIGURATION ---
# This list will store the conversation history
conversation_history = [
    {"role": "system", "content": "You are Ridhu's friendly ECE assistant. Address him as Ridhu. Remember previous details he tells you about his projects or studies."}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    try:
        user_input = request.json.get("message")
        
        # 1. Add user's new message to memory
        conversation_history.append({"role": "user", "content": user_input})
        
        # 2. Keep only the last 10 messages + the System Prompt
        # This prevents the "Brain" from getting overloaded
        if len(conversation_history) > 11:
            conversation_history = [conversation_history[0]] + conversation_history[-10:]

        # 3. Send the WHOLE history to Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )
        
        reply = completion.choices[0].message.content
        
        # 4. Add the Assistant's reply to memory so he remembers what he said
        conversation_history.append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": "Sorry Ridhu, my memory circuits glitched."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
