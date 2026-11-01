import re
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="ShopKart Support API")
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM = "You are ShopKart support. Be brief and friendly."

class Q(BaseModel):
    message: str

def mask_pii(text: str) -> str:
    text = re.sub(r"\b\d{10,16}\b", "[NUMBER]", text)          # phone/card numbers
    return re.sub(r"[\w.]+@[\w.]+", "[EMAIL]", text)

@app.post("/chat")
def chat(q: Q):
    msg = mask_pii(q.message)
    r = llm.chat.completions.create(
        model="shopkart",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": msg}],
        temperature=0.3, max_tokens=250)
    return {"reply": r.choices[0].message.content}

@app.post("/chat/stream")
def chat_stream(q: Q):
    msg = mask_pii(q.message)
    def gen():
        for chunk in llm.chat.completions.create(
                model="shopkart", stream=True,
                messages=[{"role": "system", "content": SYSTEM},
                          {"role": "user", "content": msg}]):
            yield chunk.choices[0].delta.content or ""
    return StreamingResponse(gen(), media_type="text/plain")