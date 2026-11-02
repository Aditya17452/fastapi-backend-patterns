
import asyncio, json
from typing import cast

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

client = OpenAI()

async def run_agent_with_real_mcp(user_question: str):
    
    async with Client("mcp-server-fetch") as mcp_client:

        # --- Step 1: discover its real tools — NOT hardcoded by you ---
        mcp_tools = await mcp_client.list_tools()
        openai_tools = cast(list[ChatCompletionToolUnionParam], [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in mcp_tools
        ])

       
        messages: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": user_question}
        ]
        while True:
            response = client.chat.completions.create(
                model="gpt-4o", messages=messages, tools=openai_tools
            )
            msg = response.choices[0].message
            messages.append(cast(ChatCompletionMessageParam, msg.model_dump()))

            if msg.tool_calls:
                for call in msg.tool_calls:
                    if not isinstance(call, ChatCompletionMessageFunctionToolCall):
                        continue
                    args = json.loads(call.function.arguments)
                
                    result = await mcp_client.call_tool(call.function.name, args)
                    messages.append({
                        "role": "tool", "tool_call_id": call.id, "content": str(result)
                    })
                continue
            return msg.content

if __name__ == "__main__":
    answer = asyncio.run(run_agent_with_real_mcp(
        "Fetch https://en.wikipedia.org/wiki/Eiffel_Tower and tell me how tall it is."
    ))
    print(answer)