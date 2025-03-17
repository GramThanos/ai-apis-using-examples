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

# Get available models
try:
	models = client.models.list()
except Exception as e:
	print('Failed to connect to the AI server at', os.getenv('AI_SERVER_URL'))
	sys.exit(0)

print('Available Models: ')
for model in models:
	print(' - ' + model.id)

model_to_use = os.getenv('AI_SERVER_MODEL', 'llama3.1:8b')
if not model_to_use in [model.id for model in models]:
	print('[ERROR] The model', model_to_use, 'was not found on the server\'s models list')
else:
	print('[SUCCESS] The model', model_to_use, 'was found on the server\'s models list')
