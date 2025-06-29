import openai

client = openai.OpenAI(api_key="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")




try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("API Key 정상 작동! 응답:", response.choices[0].message.content)
except Exception as e:
    print("API Key 오류:", e)