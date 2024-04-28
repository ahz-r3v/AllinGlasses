from openai import OpenAI

class Kimi:

    def __init__(self):
        self.client = OpenAI(
            api_key="sk-fnE95EqSEHOolnNZq6moOQeAPZoc6PtXWp14an1lH044lEjU",
            base_url="https://api.moonshot.cn/v1",
        )
        
        self.remote_history = [
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
        ]

    def remote_chat(self, query):
        self.remote_history += [{
            "role": "user", 
            "content": query
        }]
        response = self.client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = self.remote_history,
            temperature = 0.3,
        )
        result = response.choices[0].message.content
        self.remote_history += [{
            "role": "assistant",
            "content": result
        }]
        return result

    def remote_chat_stream(self, query):
        self.remote_history += [{
            "role": "user", 
            "content": query
        }]
        response = self.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.remote_history,
            temperature=0.3,
            stream=True,
        )
        return response
        
        # collected_messages = []
        # for idx, chunk in enumerate(response):
        #     # print("Chunk received, value: ", chunk)
        #     chunk_message = chunk.choices[0].delta
        #     if not chunk_message.content:
        #         continue
        #     collected_messages.append(chunk_message)  # save the message
        #     print(f"#{idx}: {''.join([m.content for m in collected_messages])}")
        # print(f"Full conversation received: {''.join([m.content for m in collected_messages])}")

