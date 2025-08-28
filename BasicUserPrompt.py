import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
def load_api_config():
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")

    if not api_key:
        raise EnvironmentError("GENAI_API_KEY environment variable not set.")
    model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
    api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
    return api_url, api_key

system_instructions = [
    "You are a helpful assistant that responds in a friendly and concise style.",
    "If the user asks for code, provide well-formatted Python snippets."
]

def chat():
    api_url, api_key = load_api_config()
    print("Start chatting with Gemini! Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
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
            print("Gemini:", gemini_reply)
        except Exception as e:
            print("Error communicating with Gemini:", e)

if __name__ == "__main__":
    chat()