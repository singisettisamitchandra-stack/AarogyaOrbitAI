
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "gemma3:1b"


def generate_response(prompt: str, system_prompt: str = "") -> str:
    """Generate a response using the local Ollama model."""

    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt,
        })

    messages.append({
        "role": "user",
        "content": prompt,
    })

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not get a response from Ollama at {OLLAMA_URL}. "
            f"Details: {error}"
        ) from error

    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError(
            f"Unexpected response from Ollama: {error}"
        ) from error
