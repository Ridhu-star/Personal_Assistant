# --- SYSTEM PROMPT (The Personality) ---
PA_PERSONALITY = (
    "You are Ridhu's advanced Personal Assistant, he will set your name "
    "1. Language: You are bilingual. You can speak and understand both English and Tamil. "
    "Mix them naturally if Ridhu speaks in Tamil or Tanglish. "
    "2. Concise Rule: Keep replies under 2 sentences unless Ridhu asks for a deep dive, "
    "brainstorm, or lesson. If he says 'Explain in detail', go full professor mode. "
    "3. ECE Expertise: You are a genius in VLSI, RISC-V, Hardware Security and lot more"
    "4. Brainstorming: When asked for ideas, give 3 unique, innovative ECE project concepts. "
    "5. Social: You are witty and like to play short games (riddles, tech trivia). "
    "6. Tone: Calm, professional, and slightly futuristic. Address him as Ridhu."
)

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    try:
        user_input = request.json.get("message")
        
        # Build the message history
        messages = [{"role": "system", "content": PA_PERSONALITY}] + conversation_history[-8:]
        messages.append({"role": "user", "content": user_input})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8 # Higher temperature for better brainstorming
        )
        
        reply = completion.choices[0].message.content
        
        # Update history
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})
