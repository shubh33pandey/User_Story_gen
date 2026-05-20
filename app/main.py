import asyncio
from uuid import uuid4

from app.graph.workflow import create_graph
from fastapi import FastAPI
from app.API.routes import router
from app.Infrastrature.embeddings.embedding_model import (generate_embedding,get_constitution_chunks, rank_chunks)


api = FastAPI()

api.include_router(router)

# async def chat():

#     # Create graph app
#     app = create_graph()

#     print("\n====================================")
#     print("        SPEC KIT AI AGENT")
#     print("====================================")

#     print("\nType 'exit' to quit.\n")

#     while True:

#         # User input
#         user_input = input("\nYou: ")

#         # Exit condition
#         if user_input.lower() in ["exit", "quit"]:
#             print("\nGoodbye 👋")
#             break

#         # Initial state
#         initial_state = {
#             "user_input": user_input,
#             "retrieved_context": "",
#             "constitution": "",
#             "specification": "",
#             "planning": "",
#             "task": "",
#             "user_story": ""
#         }

#         try:
#             config = {
#                 "configurable": {
#                     "thread_id": f"user-session-{uuid4()}"
#                 }
#             }

#             # Run graph
#             result = await app.ainvoke(
#                 initial_state,
#                 config=config
#             )

#             print("\n====================================")
#             print("CONSTITUTION")
#             print("====================================")
#             print(result.get("constitution", ""))

#             print("\n====================================")
#             print("SPECIFICATION")
#             print("====================================")
#             print(result.get("specification", ""))

#             # print("\n====================================")
#             # print("PLANNING")
#             # print("====================================")
#             # print(result.get("planning", ""))

#             # print("\n====================================")
#             # print("TASK")
#             # print("====================================")
#             # print(result.get("task", ""))

#             print("\n====================================")
#             print("USER STORY")
#             print("====================================")
#             print(result.get("user_story", ""))

#         except Exception as e:

#             print("\nERROR:")
#             print(str(e))


# if __name__ == "__main__":
#     asyncio.run(chat())



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

        try:

            # -----------------------------------
            # STEP 1: Generate user embedding
            # -----------------------------------
            user_vector = generate_embedding(user_input)

            # -----------------------------------
            # STEP 2: Fetch constitution chunks
            # -----------------------------------
            chunks = get_constitution_chunks()

            # -----------------------------------
            # STEP 3: Rank chunks
            # -----------------------------------
            ranked_chunks = rank_chunks(
                user_vector=user_vector,
                chunks=chunks,
                top_k=5
            )

            # -----------------------------------
            # STEP 4: Create retrieved context
            # -----------------------------------
            retrieved_context = "\n\n".join([
                f"""
Heading: {chunk['heading']}

Text:
{chunk['text']}
"""
                for chunk in ranked_chunks
            ])

            # -----------------------------------
            # STEP 5: Initial state
            # -----------------------------------
            initial_state = {
                "user_input": user_input,
                "retrieved_context": retrieved_context,
                "constitution": "",
                "specification": "",
                "planning": "",
                "task": "",
                "user_story": ""
            }

            config = {
                "configurable": {
                    "thread_id": f"user-session-{uuid4()}"
                }
            }

            # -----------------------------------
            # STEP 6: Run graph
            # -----------------------------------
            result = await app.ainvoke(
                initial_state,
                config=config
            )

            print("\n====================================")
            print("RETRIEVED CONTEXT")
            print("====================================")
            print(retrieved_context)

            print("\n====================================")
            print("CONSTITUTION")
            print("====================================")
            print(result.get("constitution", ""))

            print("\n====================================")
            print("SPECIFICATION")
            print("====================================")
            print(result.get("specification", ""))

            print("\n====================================")
            print("USER STORY")
            print("====================================")
            print(result.get("user_story", ""))

        except Exception as e:

            print("\nERROR:")
            print(str(e))

if __name__ == "__main__":
    asyncio.run(chat())
