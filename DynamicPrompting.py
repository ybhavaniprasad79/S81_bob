import os
import requests
from dotenv import load_dotenv

# =====================
# DYNAMIC PROMPTING DEMO
# =====================
# In dynamic prompting, the user can add or remove example Q&A pairs during the session to influence the model's behavior on the fly.

def load_api_config():
	load_dotenv()
	api_key = os.getenv("GENAI_API_KEY")
	if not api_key:
		raise EnvironmentError("GENAI_API_KEY environment variable not set.")
	model = os.getenv("GEMINI_MODEL") or "gemini-2.0-flash"
	api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
	api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
	return api_url, api_key

def print_examples(examples):
	if not examples:
		print("No dynamic examples set.")
		return
	print("\nCurrent dynamic examples:")
	for i in range(0, len(examples), 2):
		user = examples[i]["parts"][0]["text"]
		model = examples[i+1]["parts"][0]["text"]
		print(f"  {i//2+1}. User: {user}\n     Model: {model}")

def chat():
	api_url, api_key = load_api_config()
	dynamic_examples = []
	print("\n============================")
	print(" Welcome to Gemini (Dynamic Prompting)")
	print("============================\n")
	print("You can add or remove example Q&A pairs to guide the AI's style during this session!")
	print("Commands:")
	print("  /add     - Add a new example Q&A pair")
	print("  /list    - List current examples")
	print("  /clear   - Remove all examples")
	print("  /exit    - Quit\n")
	while True:
		user_input = input("User: ")
		if user_input.lower() in ("/exit", "exit", "quit"):
			print("Goodbye! You can always come back and teach me new tricks! 🦄")
			break
		elif user_input.lower() == "/add":
			print("Enter the example user message:")
			ex_user = input("  Example User: ")
			print("Enter the example model response:")
			ex_model = input("  Example Model: ")
			dynamic_examples.append({"role": "user", "parts": [{"text": ex_user}]})
			dynamic_examples.append({"role": "model", "parts": [{"text": ex_model}]})
			print("Example added!\n")
		elif user_input.lower() == "/list":
			print_examples(dynamic_examples)
		elif user_input.lower() == "/clear":
			dynamic_examples.clear()
			print("All examples cleared!\n")
		else:
			# Build the contents with the dynamic examples and the current user input
			contents = dynamic_examples + [
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
					return
				data = resp.json()
				gemini_reply = data["candidates"][0]["content"]["parts"][0]["text"]
				print("Gemini:", gemini_reply)
			except Exception as e:
				print("Error communicating with Gemini:", e)

if __name__ == "__main__":
	chat()