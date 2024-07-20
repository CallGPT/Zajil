from openai import OpenAI

def chat_with_ai(messages):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )

    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    return response, messages
