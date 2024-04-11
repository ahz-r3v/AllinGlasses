from zhipuai import ZhipuAI
client = ZhipuAI(api_key="b17e4581067ebc9de0f3fdcc59af5884.uUVM5WJF5XAfTjAl") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "今天中午吃什么"},
    ],
)
print("问：‘今天中午吃什么’")
print(response.choices[0].message.content)