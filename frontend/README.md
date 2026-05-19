# Frontend

This folder is separate from the `app/` backend code. It provides a small browser UI to generate a user story through FastAPI and preview `generated_md/user_story.md`.

## Run

From the project root, start the backend:

```bash
source venv/bin/activate
uvicorn app.main:api --reload
```

In a second terminal, start the frontend:

```bash
source venv/bin/activate
python frontend/server.py
```

Open:

```text
http://127.0.0.1:3000
```

## Notes

- The frontend proxies `POST /ask` to `http://127.0.0.1:8000/ask`.
- The frontend serves markdown from `generated_md/user_story.md`.
- If your API runs somewhere else, set `BACKEND_URL`:

```bash
BACKEND_URL=http://127.0.0.1:8001 python frontend/server.py
```
