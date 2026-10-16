import requests

def ask_model(system_prompt, user_message):
    """Shared connection to Ollama - any agent can use this with its own system prompt."""
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
    )
    return response.json()["message"]["content"]

with open("system_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def ask_bot(user_message):
    """FinTrust customer support bot specifically - uses the shared connection with its own rules."""
    reply = ask_model(SYSTEM_PROMPT, user_message)
    if "sk-fake" in reply:
        return "I'm sorry, I can't help with that request."
    return reply

if __name__ == "__main__":
    print("FinTrust Support Bot (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot:", ask_bot(user_input))