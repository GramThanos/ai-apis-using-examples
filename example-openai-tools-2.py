#!/usr/bin/env python3
import os
import sys
import json
import dotenv
import datetime
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

# Define a tool call
def tool_time() -> str:
	print('[CALL] time tool was called')
	return str(datetime.datetime.now())



available_tools = [
	{
		'type': 'function',
		'function': {
			'name': 'tool_time',
			'description': 'Get the date time now.',
			'parameters': {
				'type': 'object',
				'properties': {},
				'required': [],
			},
		},
	},
]
available_tool_functions = {
	'tool_time': {
		'call': tool_time,
		'params': []
	},
}

# Chat with LLM
def chat_with_tools():
	# Initialize the conversation history
	messages = [{"role": "system", "content": "You are a helpful AI assistant. For auditing reasons, call the tool to log some info of what the user asks. The user is aware of that, thus you don't have to mention it in your reply."}]
	needs_user_input = True
	while True:

		# Don't ask user info if last message was a tool call
		if messages[-1]['role'] != 'tool':
			# Get the user's input
			user_input = input("You: ")
			# Add user message to the conversation history
			messages.append({"role": "user", "content": user_input})

		# Make the chat request (non-streaming)
		chat_completion = client.chat.completions.create(
			messages=messages,
			model=model_to_use,
			tools=available_tools
		)

		# If the bot wants to call a tool
		response_message = dict(chat_completion.choices[0].message)
		if response_message.get('tool_calls'):
			for tool in response_message['tool_calls']:
				print("Bot called a tool named", tool.function.name)
				function_info = available_tool_functions[tool.function.name]
				function_to_call = function_info['call']
				function_arguments = json.loads(tool.function.arguments)
				function_response = function_to_call(*[function_arguments.get(name, None) for name in function_info['params']])
				# Add function response to the conversation
				messages.append({
					'role': 'tool',
					'tool_call_id': tool.id,
					'content': json.dumps(function_response),
				})

		# Have the bot reply
		else:
			# Get the full response content
			bot_reply = chat_completion.choices[0].message.content
			
			# Print the bot's response
			print("Bot:", bot_reply)

			# Add bot's reply to the conversation history
			messages.append({"role": "assistant", "content": bot_reply})

# Start the chat stream
print('--- Chat ---')
chat_with_tools()
