from dotenv import load_dotenv
import os

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral").lower()


def _load_mistral_llm():
    try:
        from langchain_mistralai import ChatMistralAI
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency 'langchain-mistralai'. Install it with "
            "`pip install -r requirements.txt` or set LLM_PROVIDER=ollama."
        ) from exc

    return ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
        temperature=0,
        api_key=os.getenv("MISTRAL_API_KEY"),
    )


def _load_ollama_llm():
    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
        temperature=0,
    )


if LLM_PROVIDER == "mistral":
    llm = _load_mistral_llm()
elif LLM_PROVIDER == "ollama":
    llm = _load_ollama_llm()
else:
    raise ValueError("LLM_PROVIDER must be either 'mistral' or 'ollama'.")


# llm = ChatOllama(
#     model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
#     temperature=0,
# )


# llm = ChatOllama(
#     model=os.getenv("OLLAMA_MODEL", "deepseek-r1:latest"),
#     temperature=0,
# )
