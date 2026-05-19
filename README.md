# Gen User Story

AI agent for generating Scrum-oriented project artifacts such as constitutions, specifications, and user stories from natural language input. The backend uses FastAPI, LangGraph, LangChain, and configurable LLM providers.

## Features

- Generate constitution, specification, and user story markdown outputs.
- Run as an interactive CLI with `python -m app.main`.
- Run as a FastAPI backend with a lightweight browser frontend.
- Supports Mistral API by default and local Ollama through environment configuration.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your API key or switch to Ollama.

## Run CLI

```bash
source venv/bin/activate
python -m app.main
```

## Run Web App

Start the backend:

```bash
source venv/bin/activate
uvicorn app.main:api --reload
```

Start the frontend in another terminal:

```bash
source venv/bin/activate
python frontend/server.py
```

Open `http://127.0.0.1:3000`.

## Environment Variables

- `LLM_PROVIDER`: `mistral` or `ollama`.
- `MISTRAL_API_KEY`: Required when using Mistral.
- `MISTRAL_MODEL`: Optional Mistral model name.
- `OLLAMA_MODEL`: Optional Ollama model name.

## GitHub Safety

Do not commit `.env`, `venv/`, caches, or local secrets. These are ignored by `.gitignore`.
