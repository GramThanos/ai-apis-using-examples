#!/usr/bin/env python3
import os
import sys
import dotenv
from openai import OpenAI
dotenv.load_dotenv()

# Configure client to connect to the Ollama server running in UNIPI
client = OpenAI(
	base_url = os.getenv('AI_SERVER_URL'),
	api_key= os.getenv('AI_SERVER_API_KEY')
)

# Check available models
try:
	models = client.models.list()
except Exception as e:
	print('Failed to connect to the AI server at', os.getenv('AI_SERVER_URL'))
	sys.exit(0)

model_to_use = os.getenv('AI_SERVER_MODEL', 'llama3.1:8b')
if not model_to_use in [model.id for model in models]:
	print('Error! Model', model_to_use, 'was not found on server.')
	sys.exit(0)

# Chat with LLM in a streaming way
def chat_stream():
	# Initialize the conversation history
	messages = []

	while True:
		# Get the user's input
		user_input = input("You: ")

		# Add user message to the conversation history
		messages.append({"role": "user", "content": user_input})

		# Make the chat request with streaming enabled
		chat_completion = client.chat.completions.create(
			messages=messages,
			model=model_to_use,
			stream=True  # Enable streaming
		)

		# Process the response as it streams and print it in real-time
		response_content = ""
		for chunk in chat_completion:
			if hasattr(chunk, 'choices'):
				for choice in chunk.choices:
					if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
						# Stream the content of the response
						print(choice.delta.content, end='', flush=True)

		print('') # Print a newline after the bot's response

		# Add bot's reply to the conversation history
		messages.append({"role": "assistant", "content": response_content.strip()})

# Start the chat stream
print('--- Chat ---')
chat_stream()
