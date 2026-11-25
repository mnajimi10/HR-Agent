import json
import logging
import time

from openai import OpenAI

from config import LLM_API_KEY, LLM_MODEL
from schemas import AskResponse

logger = logging.getLogger("agent")

SYSTEM_PROMPT = "Tu es un assistant RH. Réponds en français, de façon claire et concise."

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",     
    timeout=120,          
    max_retries=2,
)

def ask_llm(question: str) -> AskResponse:
    start = time.perf_counter()

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=500, 
    )

    duration_ms = round((time.perf_counter() - start) * 1000)
    usage = resp.usage

    logger.info(json.dumps({
        "event": "llm_call",
        "model": LLM_MODEL,
        "duration_ms": duration_ms,
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
    }))

    return AskResponse(
        answer=resp.choices[0].message.content or "",
        model=LLM_MODEL,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
    )