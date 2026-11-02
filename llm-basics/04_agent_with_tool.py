from langchain_groq import ChatGroq 
from dotenv import load_dotenv
from langchain.agents import create_agent 
from langchain.tools import tool

load_dotenv()
import os 
llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY"))

@tool 
def addition(a:int,b:int) ->int:
    '''It give addition of two numbers.'''

    return (a+b)

agent=create_agent(model=llm,tools=[addition],system_prompt="This is the addition tool.")
m={"messages":[{"role":"user","content":"Give me what come after combine 24 and 56 ?"}]} 
response=agent.invoke(m)
final_message = response["messages"][-1]

print(final_message.content)
