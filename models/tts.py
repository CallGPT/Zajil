from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input="ازاي اقدر اساعدك النهارده؟",
)

response.stream_to_file("output1.mp3")