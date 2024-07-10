from groq import Groq

from src.utils import getenv


class GroqManager:
    _instance = None

    LLAMA3_8B = "llama3-8b-8192"
    LLAMA3_70B = "llama3-70b-8192"
    MIXTRAL = "mixtral-8x7b-32768"
    GEMMA = "gemma-7b-it"
    WHISPER = "whisper-large-v3"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GroqManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, model=LLAMA3_70B):
        self.client = Groq(api_key=getenv('GROQ_API_KEY'))
        self.model = model
        pass

    def text(self, system_message, user_message, temp, model=None):
        if model is None:
            model = self.model

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model=model,
            temperature=temp,
        )

        return chat_completion.choices[0].message.content

    def json(self, system_message, user_message, temp, model=None):
        if model is None:
            model = self.model

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model=model,
            temperature=temp,
            response_format={"type": "json_object"},
        )

        return chat_completion.choices[0].message.content
