import os
import requests
from dotenv import load_dotenv

# =====================
# ONE-SHOT PROMPTING DEMO
# =====================
# In zero-shot prompting, only the user's message is sent to the model.
# In one-shot prompting, we provide a single example conversation to guide the model's style and behavior.

def load_api_config():
	load_dotenv()
	api_key = os.getenv("GENAI_API_KEY")
	if not api_key:
		raise EnvironmentError("GENAI_API_KEY environment variable not set.")
	model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
	api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
	api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
	return api_url, api_key

# Adorable one-shot example: user asks for a cute animal fact, assistant responds in a friendly, playful way
one_shot_example = [
	{
		"role": "user",
		"parts": [
			{"text": "Can you tell me a fun fact about cats?"}
		]
	},
	{
		"role": "model",
		"parts": [
			{"text": "Absolutely! Did you know that cats have a special purr that can calm both themselves and their humans? 🐾 Isn't that adorable!"}
		]
	}
]

def chat():
	api_url, api_key = load_api_config()
	print("\n============================")
	print(" Welcome to Gemini (One-Shot)")
	print("============================\n")
	print("This chatbot uses one-shot prompting: it always includes a cute example conversation to guide the AI's style!\nType 'exit' to quit.\n")
	while True:
		user_input = input("User: ")
		if user_input.lower() in ("exit", "quit"):
			print("Goodbye! Stay pawsitive! 🐾")
			break
		# Build the contents with the one-shot example and the current user input
		contents = one_shot_example + [
			{
				"role": "user",
				"parts": [
					{"text": user_input}
				]
			}
		]
		payload = {"contents": contents}
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