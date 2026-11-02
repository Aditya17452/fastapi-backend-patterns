from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from dotenv import load_dotenv
load_dotenv()
import os 
import json
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def addition(a:int,b:int)->int:
    '''It give addition of two numbers.'''
    return (a+b)

tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "addition",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
            },
        },
    }
]

def run_agent():
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        }
    ]

    while True:

        user = input("You: ")

        if user.lower() == "exit":
            print("Bye....")
            break

        messages.append({
            "role": "user",
            "content": user,
        })

        while True:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            message = response.choices[0].message

            messages.append(message)
            if not message.tool_calls:

                print("Agent:", message.content)
                break
            for tool_call in message.tool_calls:

                if tool_call.function.name == "addition":

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    result = addition(**arguments)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })


if __name__ == "__main__":
    run_agent()                    