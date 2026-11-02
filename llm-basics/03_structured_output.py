from langchain_core.prompts import ChatPromptTemplate 
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
load_dotenv()
from pydantic import BaseModel 
class Info(BaseModel):
    role:str
    topic:str
    explanation:str
    num:int
    name:list[str]
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)
prompt=ChatPromptTemplate.from_messages( [
    ("system","You are a {role} engineer. Return the name fields as a list of strings."),
    ("human","what is {topic}?")]
)
structured_llm=llm.with_structured_output(Info)
chain =prompt|structured_llm 
r=chain.invoke({
    "role":"software",
    "topic":"langchain"})
print(r)