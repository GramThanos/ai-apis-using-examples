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

show_thinking_info = False

# Chat with LLM in a streaming way
def chat_stream():
	# Prepare for Chain of Thought Prompting
	# Prompt from https://medium.com/@harishhacker3010/can-we-make-any-smaller-opensource-ai-models-smarter-than-human-1ea507e644a0
	system_prompt_cot = "Begin by enclosing all thoughts within <thinking> tags, exploring multiple angles and approaches. Break down the solution into clear steps within <step> tags. Start with a 20-step budget, requesting more for complex problems if needed. Use <count> tags after each step to show the remaining budget. Stop when reaching 0. Continuously adjust your reasoning based on intermediate results and reflections, adapting your strategy as you progress. Regularly evaluate progress using <reflection> tags. Be critical and honest about your reasoning process. Assign a quality score between 0.0 and 1.0 using <reward> tags after each reflection. Use this to guide your approach: 0.8+: Continue current approach 0.5-0.7: Consider minor adjustments Below 0.5: Seriously consider backtracking and trying a different approach If unsure or if reward score is low, backtrack and try a different approach, explaining your decision within <thinking> tags. For mathematical problems, show all work explicitly using LaTeX for formal notation and provide detailed proofs. Explore multiple solutions individually if possible, comparing approaches in reflections. Use thoughts as a scratchpad, writing out all calculations and reasoning explicitly. Synthesize the final answer within <answer> tags, providing a clear, concise summary. Conclude with a final reflection on the overall solution, discussing effectiveness, challenges, and solutions. Assign a final reward score."
	system_prompt_assistant = "You are a helpful assistant. Before answering take into account your <thinking>. Respond in a friendly, yet professional tone."
	system_message = {"role": "system", "content": None}
	
	# Initialize the conversation history
	messages = [system_message]

	while True:
		# Get the user's input
		print(
			'┌────────────────────────────────────────────────┐\n'+
			'│ User input                                     │\n'+
			'└────────────────────────────────────────────────┘'
		)
		user_input = input('')

		# Add user message to the conversation history
		messages.append({"role": "user", "content": user_input})



		# Starting thinking process
		system_message['content'] = system_prompt_cot
		chat_completion = client.chat.completions.create(
			messages=messages,
			model=model_to_use,
			stream=True
		)

		# Process the thinking as it streams and print it in real-time
		print(
			'┌────────────────────────────────────────────────┐\n'+
			'│ Bot is Thinking ...                            │\n'+
			'└────────────────────────────────────────────────┘'
		)
		response_content = ""
		for chunk in chat_completion:
			if hasattr(chunk, 'choices'):
				for choice in chunk.choices:
					if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
						# Stream the content of the thinking
						if (show_thinking_info):
							print(choice.delta.content, end='', flush=True)
		if (show_thinking_info):
			print('')

		# Add bot's reply to the conversation history
		messages.append({"role": "assistant", "content": response_content.strip()})



		# Process thinking to add a response
		system_message['content'] = system_prompt_assistant
		chat_completion = client.chat.completions.create(
			messages=messages,
			model=model_to_use,
			stream=True
		)

		# Process the response as it streams and print it in real-time
		print(
			'┌────────────────────────────────────────────────┐\n'+
			"│ Bot's answering                                │\n"+
			'└────────────────────────────────────────────────┘'
		)
		response_content = ""
		for chunk in chat_completion:
			if hasattr(chunk, 'choices'):
				for choice in chunk.choices:
					if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
						# Stream the content of the response
						print(choice.delta.content, end='', flush=True)
		print('')

		# Remove thinking from history
		del messages[-1]

		# Add bot's reply to the conversation history
		messages.append({"role": "assistant", "content": response_content.strip()})

# Start the chat stream
print('--- Chat ---')
chat_stream()
