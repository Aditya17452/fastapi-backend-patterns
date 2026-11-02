from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 
load_dotenv()
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain.messages import SystemMessage, HumanMessage,AIMessage
from langchain.agents import create_agent 

@tool
def addition(a:int,b:int)->int:
    '''It give addition of two numbers.'''
    return (a+b)
@tool
def subtraction(a:int,b:int)->int:
    '''It give subtraction of two numbers.'''
    return (a-b) 

message=[SystemMessage(content="You are a helpful assistant with add on skills of addition and subtraction tools.")]
model=ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")

)
agent=create_agent(model=model,tools=[addition,subtraction],system_prompt="You are a helpful assistant with add on skills of addition and subtraction tools.")

def chatboat(input:str)->str:
    
    message.append(HumanMessage(content=input))
    r=agent.invoke({"messages":message })
    message.append(AIMessage(content=r["messages"][-1].content))
    return r


if __name__=="__main__":
    while True:
        user=input("You: ")
        if user.lower()=="exit":
            print("Bye....")
            break
        response=chatboat(user)
        print("Agent:",response["messages"][-1].content)