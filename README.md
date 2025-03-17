# AI APIs Examples
Example codes to interact with popular AI-related APIs.

## Examples
Here is a list of examples:

- Using OpenAI server API:
	- list server models [example](example-openai-list-models.py)
	- simple chat [example](example-openai-chat.py)
	- simple chat with streaming tokens [example](example-openai-chat-stream.py)
	- simple chat with custom sytem prompt and streaming tokens [example](example-openai-system-streaming.py)
	- simple chat with thinking chain-of-though step and streaming tokens [example](example-openai-thinking-stream.py)
	- simple chat with tools functionality [example](example-openai-tools.py)

## Setup

First install the dependencies:

```bash
python3 -m pip install -r ./requirements.txt
```

Configure your servers and/or API keys, copy the example `.env.template` and change the values: 
```bash
cp .env.template .env
nano .env
```

### Ollama .env
Example values for an [Ollama](https://ollama.com/) server:
```
AI_SERVER_URL=http://ollama-server-domain:port/v1
AI_SERVER_API_KEY=ollama
AI_SERVER_MODEL=llama3.1:8b
```

### Gemini .env
Example values for Google's [Gemini](https://ai.google.dev/gemini-api/docs/api-key):
```
AI_SERVER_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AI_SERVER_API_KEY=GEMINI_API_KEY_HERE
AI_SERVER_MODEL=models/gemini-2.0-flash
```

### OpenAI ChatGPT .env
Example values for OpenAI's [ChatGPT](https://platform.openai.com/docs/api-reference/introduction):
```
AI_SERVER_URL=https://api.openai.com/v1
AI_SERVER_API_KEY=OPENAI_API_KEY_HERE
AI_SERVER_MODEL=gpt-4o
```

## Run the example you want

Checking connectivity and server models:
```bash
python3 ./example-openai-list-models.py
```

Running an example:
```bash
python3 ./example-openai-chat.py
```
