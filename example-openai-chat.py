#!/usr/bin/env python3
import os
import sys
import dotenv
from openai import OpenAI
dotenv.load_dotenv()

# Configure client to connect to the AI server
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
def chat():
	# Initialize the conversation history
	messages = []

	while True:
		# Get the user's input
		user_input = input("You: ")

		# Add user message to the conversation history
		messages.append({"role": "user", "content": user_input})

		# Make the chat request (non-streaming)
		chat_completion = client.chat.completions.create(
			messages=messages,
			model=model_to_use
		)

		# Get the full response content
		bot_reply = chat_completion.choices[0].message.content
		
		# Print the bot's response
		print("Bot:", bot_reply)

		# Add bot's reply to the conversation history
		messages.append({"role": "assistant", "content": bot_reply})

# Start the chat stream
print('--- Chat ---')
chat()
