import os
import requests
from dotenv import load_dotenv

# =====================
# TOKEN COUNTING DEMO
# =====================
# This script estimates and displays the number of tokens used in each prompt and response.
# (For demonstration, tokens are estimated as words split by whitespace.)

def load_api_config():
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("GENAI_API_KEY environment variable not set.")
    model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
    api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
    return api_url, api_key

def count_tokens(text):
    # Simple token estimation: split by whitespace
    return len(text.split())

def chat():
    api_url, api_key = load_api_config()
    print("\n============================")
    print(" Welcome to Gemini (Token Counting Demo)")
    print("============================\n")
    print("This chatbot estimates and displays the number of tokens (words) used in each prompt and response.\nType 'exit' to quit.\n")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye! Token counting session ended.")
            break
        prompt_tokens = count_tokens(user_input)
        print(f"[Prompt tokens used: {prompt_tokens}]")
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": user_input}
                    ]
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
        try:
            resp = requests.post(api_url, json=payload, headers=headers)
            if resp.status_code != 200:
                print(f"Error: {resp.status_code} - {resp.reason}")
                try:
                    print("Details:", resp.json())
                except Exception:
                    print("Response:", resp.text)
                continue
            data = resp.json()
            gemini_reply = data["candidates"][0]["content"]["parts"][0]["text"]
            response_tokens = count_tokens(gemini_reply)
            print(f"Gemini: {gemini_reply}")
            print(f"[Response tokens used: {response_tokens}]\n")
        except Exception as e:
            print("Error communicating with Gemini:", e)

if __name__ == "__main__":
    chat()