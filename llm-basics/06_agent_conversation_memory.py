import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent


load_dotenv()


@tool
def addition(a: int, b: int) -> int:
    """It gives addition of two numbers."""
    return a + b


model = ChatOpenAI(
    model="gpt-4o-mini"
)

agent = create_agent(
    model=model,
    tools=[addition],
    system_prompt="You are a helpful assistant with an addition tool."
)

m = []

while True:

    user = input("You: ")

    if user.lower() == "exit":
        print("Bye....")
        break

    m.append({
        "role": "user",
        "content": user
    })

    response = agent.invoke({
        "messages": m
    })

    
    messages = response["messages"]

    for message in messages:
        print("\nTYPE:", type(message).__name__)
        print("CONTENT:", message.content)

        if hasattr(message, "tool_calls"):
            print("TOOL CALLS:", message.tool_calls)

        print("-" * 50)

    

   
    m = messages