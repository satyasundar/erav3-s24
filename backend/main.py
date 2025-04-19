from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agentic_prompt

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process")
async def process_prompt(req: Request):
    data = await req.json()
    prompt = data.get("prompt")
    messages = data.get("messages")

    # print("***Received prompt:", prompt)
    # print("***Received messages:", messages)

    result = run_agentic_prompt(prompt, messages)
    return {"result": result}
