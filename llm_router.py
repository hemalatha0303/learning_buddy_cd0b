# llm_router.py
import requests
from dotenv import load_dotenv
load_dotenv()
import os
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class FlashcardLLMRouter:
    @staticmethod
    def generate(prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.3, max_tokens=1024):
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": "You are an expert flashcard generator."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]
