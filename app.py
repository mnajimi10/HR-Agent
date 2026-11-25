import logging

from flask import Flask, jsonify, request
from openai import APIError, APITimeoutError, RateLimitError
from pydantic import ValidationError

from llm import ask_llm
from schemas import AskRequest

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask():
    try:
        payload = AskRequest.model_validate(request.get_json(silent=True) or {})
    except ValidationError as e:
        return jsonify(error="invalid_request",
                       details=e.errors(include_url=False, include_context=False)), 400

    try:
        result = ask_llm(payload.question)
    except RateLimitError as e:
        logging.error("RateLimitError: %s", e)
        return jsonify(error="llm_rate_limited", message="Service saturé, réessayez."), 503
    except APITimeoutError:
        return jsonify(error="llm_timeout", message="Le modèle a mis trop de temps."), 504
    except APIError as e:
        logging.error("APIError: %s", e)
        return jsonify(error="llm_error", message="Erreur du fournisseur LLM."), 502

    return jsonify(result.model_dump())

if __name__ == "__main__":
    app.run(debug=True)