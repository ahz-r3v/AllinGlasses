import requests
import json

def chat(query):
   # Get a response using a prompt with streaming
   payload = {
   "model": "./dist/Qwen-1_8B-Chat-q4f16_1-MLC/",
   "messages": [{"role": "user", "content": query}],
   "stream": False,
   }
   r = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=payload)
   choices = r.json()["choices"]
   for choice in choices:
      print(f"{choice['message']['content']}\n")

def chat_stream(query):
   # Get a response using a prompt with streaming
   payload = {
   "model": "./dist/Llama-2-7b-chat-hf-q4f16_1-MLC/",
   "messages": [{"role": "user", "content": query}],
   "stream": True,
   }
   with requests.post("http://127.0.0.1:8080/v1/chat/completions", json=payload, stream=True) as r:
      for chunk in r.iter_content(chunk_size=None):
         chunk = chunk.decode("utf-8")
         if "[DONE]" in chunk[6:]:
            break
         response = json.loads(chunk[6:])
         content = response["choices"][0]["delta"].get("content", "")
         print(content, end="", flush=True)
   print("\n")
