from pydantic import BaseModel
from fastapi import APIRouter
from uuid import uuid4

from app.graph.workflow import create_graph

router = APIRouter()
graph_app = create_graph()


class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(data: ChatRequest):

    # Initial graph state
    initial_state = {
        "user_input": data.question,
        "retrieved_context": "",
        "constitution": "",
        # "specification": "",
        # "planning": "",
        # "task": "",
        "user_story": ""
    }

    try:

        config = {
            "configurable": {
                "thread_id": f"user-session-{uuid4()}"
            }
        }

        # Run workflow graph
        result = await graph_app.ainvoke(
            initial_state,
            config=config
        )

        # Return JSON response
        return {
            "success": True,
            "input": data.question,
            # "constitution": result.get("constitution", ""),
            # "specification": result.get("specification", ""),
            # "planning": result.get("planning", ""),
            # "task": result.get("task", ""),
            "user_story": result.get("user_story", "")
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
