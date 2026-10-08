import os
import logging
from fastapi import FastAPI, Request
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

DEEPSEEK_API_URL = "https://api.aitunnel.ru/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    if not user_text or user_text.strip() == "":
        return {
            "version": body["version"],
            "session": body["session"],
            "response": {
                "end_session": False,
                "text": "Привет! Спроси меня о чём-нибудь."
            }
        }

    response = requests.post(
        DEEPSEEK_API_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-v4.1-flash",
            "messages": [{"role": "user", "content": user_text}],
        }
    )

    # ← ОТЛАДКА: посмотреть, что вернул AITUNNEL
    logger.info("STATUS: %s", response.status_code)
    logger.info("BODY: %s", response.text)

    answer = response.json()["choices"][0]["message"]["content"]

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
