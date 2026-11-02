from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))
m=[{"role":"system","content":"You are an helpful assistant."}]


while True:
    i=input("You: ")
    if i.lower()=="exit":
        print("Byy....")
        break
    m1={"role":"user","content":i}
    m.append(m1)
    r=client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=m )
    print(r.choices[0].message.content)





