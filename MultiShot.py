import os
import requests
from dotenv import load_dotenv

# =====================
# MULTI-SHOT PROMPTING DEMO
# =====================
# In multi-shot prompting, we provide several example conversations to guide the model's style and behavior.

def load_api_config():
	load_dotenv()
	api_key = os.getenv("GENAI_API_KEY")
	if not api_key:
		raise EnvironmentError("GENAI_API_KEY environment variable not set.")
	model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
	api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
	api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
	return api_url, api_key

# Multi-shot examples: several cute, friendly Q&A pairs
multi_shot_examples = [
	# Example 1
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
	},
	# Example 2
	{
		"role": "user",
		"parts": [
			{"text": "What's something interesting about dogs?"}
		]
	},
	{
		"role": "model",
		"parts": [
			{"text": "Of course! Dogs have an amazing sense of smell—up to 100,000 times better than humans! 🐶 They can even detect some diseases."}
		]
	},
	# Example 3
	{
		"role": "user",
		"parts": [
			{"text": "Do you know a cute fact about pandas?"}
		]
	},
	{
		"role": "model",
		"parts": [
			{"text": "Yes! Baby pandas are born pink, blind, and tiny—about the size of a stick of butter! 🐼 They grow up to be big and fluffy."}
		]
	}
]

def chat():
	api_url, api_key = load_api_config()
	print("\n============================")
	print(" Welcome to Gemini (Multi-Shot)")
	print("============================\n")
	print("This chatbot uses multi-shot prompting: it always includes several adorable example conversations to guide the AI's style!\nType 'exit' to quit.\n")
	while True:
		user_input = input("User: ")
		if user_input.lower() in ("exit", "quit"):
			print("Goodbye! Stay curious and cuddly! 🐾")
			break
		# Build the contents with the multi-shot examples and the current user input
		contents = multi_shot_examples + [
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