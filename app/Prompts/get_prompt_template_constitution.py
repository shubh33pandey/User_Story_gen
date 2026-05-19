from langchain_core.prompts import ChatPromptTemplate


CONSTITUTION_GENERATOR_PROMPT = ChatPromptTemplate.from_template("""
                                                                 
Inputs:
User Request:
{user_input}

Retrieved Context:
{retrieved_context}
I want to create a concise and context-specific Constitution File based on the Global Constitution.

The new Constitution File should be directly relevant to the user-provided prompt, removing any unnecessary or unrelated sections while preserving the core governance rules, structure, quality standards, and execution principles.

The output should be professional, focused, reusable, and suitable for guiding an AI agent to generate consistent, high-quality results for the specific user request.
                                                                 
                                                                 


""")
