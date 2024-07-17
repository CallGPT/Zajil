from elevenlabs import save
from elevenlabs.client import ElevenLabs


def generatVoice(text, filename, voice="Dan Dan"):
    client = ElevenLabs(api_key="sk_b912bfab77e1f6d7eb3e18bf568bc0f1f64dcbe97c6ffeff")
    audio = client.generate(
        text=text,
        voice="Harry",
        model="eleven_multilingual_v2"
    )
    save(audio, filename)

