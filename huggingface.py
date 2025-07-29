import os
import requests
from dotenv import load_dotenv
import utils

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "moonshotai/Kimi-K2-Instruct:novita"
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
}
INJECTED_MESSAGE = f"""\n
additional information about the environment:
date and time (in utc) is {utils.get_utc_datetime()}
"""

def get_model_response(system_prompt:str ,message: str):
    print(system_prompt + INJECTED_MESSAGE)
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt + INJECTED_MESSAGE},
            {"role": "user", "content": message}
        ],
        "model": MODEL
    }
    
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    choices = response.json().get("choices", [])
    if not choices:
        raise Exception("invalid AI response")
    
    response_content = choices[0]["message"]["content"]

    if len(response_content) > 2000:
        response_content = response_content[:1800] + "- blah blah blah... aint typing alot :yawning_face:"
        
    return response_content
