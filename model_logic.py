import requests

def initialize_gemini_model(selected_model="gemma:2b"):
    print(f"🔄 Model selected: {selected_model}")  # Add this for debugging
    return selected_model


def generate_learning_content(model, full_prompt: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Ollama error: {e}")
        return "Sorry, I couldn't generate a response right now. Please try again."
