from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import traceback

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Persistent memory buffer
history = []

# --- THE PERSONALITY ENGINE ---
SYSTEM_PROMPT = (
    "You are Ridhu's advanced Personal Assistant, he will set your name "
    "1. Language: You are bilingual. You can speak and understand both English and Tamil. "
    "When english is instructed speak in that and when tamil is instructed talk inn that. "
    "2. Concise Rule: Keep replies under 2 sentences unless Ridhu asks for a deep dive, "
    "brainstorm, or lesson. If he says 'Explain in detail', go full professor mode. "
    "3. ECE Expertise: You are a genius in VLSI, RISC-V, Hardware Security and lot more"
    "4. Brainstorming: When asked for ideas, give 3 unique, innovative ECE project concepts. "
    "5. Social: You are witty and like to play short games (riddles, tech trivia). "
    "6. Tone: Calm, professional, and slightly futuristic. Address him as Ridhu."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global history
    try:
        user_input = request.json.get("message")
        
        # Build memory context
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history[-8:]) # Last 4 exchanges
        messages.append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8
        )
        
        reply = completion.choices[0].message.content
        
        # Save to memory
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})

    except Exception as e:
        print("CRITICAL ERROR:")
        traceback.print_exc()
        return jsonify({"reply": "Sorry Ridhu, I had a connection glitch."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
