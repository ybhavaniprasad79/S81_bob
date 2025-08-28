import os
import requests
from dotenv import load_dotenv
import datetime

# =====================
# FUNCTION CALLING DEMO
# =====================
# This script demonstrates basic function calling: the model can request a function, and the script executes it.

# Example functions

def get_time():
    return f"Current time is: {datetime.datetime.now().strftime('%H:%M:%S')}"

def add_numbers(a, b):
    return f"Sum: {a + b}"

def load_api_config():
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("GENAI_API_KEY environment variable not set.")
    model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
    api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
    return api_url, api_key

# Simple function calling parser (looks for keywords in model response)
def handle_function_call(response):
    response = response.lower()
    if "get_time" in response:
        return get_time()
    elif "add_numbers" in response:
        # Example: "add_numbers(3, 5)"
        import re
        match = re.search(r"add_numbers\((\d+),\s*(\d+)\)", response)
        if match:
            a, b = int(match.group(1)), int(match.group(2))
            return add_numbers(a, b)
        else:
            return "Couldn't parse numbers for add_numbers."
    return None

def chat():
    api_url, api_key = load_api_config()
    print("\n============================")
    print(" Welcome to Gemini (Function Calling Demo)")
    print("============================\n")
    print("Ask the model to call a function, e.g.:\n  get_time\n  add_numbers(3, 5)\nType 'exit' to quit.\n")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye! Function calling session ended.")
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
            print(f"Gemini: {gemini_reply}")
            # Check if the model is requesting a function call
            result = handle_function_call(gemini_reply)
            if result:
                print(f"[Function result]: {result}\n")
        except Exception as e:
            print("Error communicating with Gemini:", e)

if __name__ == "__main__":
    chat()