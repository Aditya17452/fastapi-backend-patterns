from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
load_dotenv()
llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
m=[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"how are you?"}]
r=llm.invoke(m)
print(r)

