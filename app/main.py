import asyncio
from uuid import uuid4

from app.graph.workflow import create_graph
from fastapi import FastAPI
from app.API.routes import router

api = FastAPI()

api.include_router(router)

async def chat():

    # Create graph app
    app = create_graph()

    print("\n====================================")
    print("        SPEC KIT AI AGENT")
    print("====================================")

    print("\nType 'exit' to quit.\n")

    while True:

        # User input
        user_input = input("\nYou: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye 👋")
            break

        # Initial state
        initial_state = {
            "user_input": user_input,
            "retrieved_context": "",
            "constitution": "",
            "specification": "",
            "planning": "",
            "task": "",
            "user_story": ""
        }

        try:
            config = {
                "configurable": {
                    "thread_id": f"user-session-{uuid4()}"
                }
            }

            # Run graph
            result = await app.ainvoke(
                initial_state,
                config=config
            )

            print("\n====================================")
            print("CONSTITUTION")
            print("====================================")
            print(result.get("constitution", ""))

            print("\n====================================")
            print("SPECIFICATION")
            print("====================================")
            print(result.get("specification", ""))

            # print("\n====================================")
            # print("PLANNING")
            # print("====================================")
            # print(result.get("planning", ""))

            # print("\n====================================")
            # print("TASK")
            # print("====================================")
            # print(result.get("task", ""))

            print("\n====================================")
            print("USER STORY")
            print("====================================")
            print(result.get("user_story", ""))

        except Exception as e:

            print("\nERROR:")
            print(str(e))


if __name__ == "__main__":
    asyncio.run(chat())
