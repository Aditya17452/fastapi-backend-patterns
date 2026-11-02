# LLM Basics

Short, runnable scripts that build up from a plain LLM call to tool-using agents and MCP. Each file focuses on one idea.

| # | Script | Concept |
|---|---|---|
| 01 | `01_groq_chat.py` | Multi-turn chat with the Groq SDK, keeping conversation history |
| 02 | `02_langchain_openrouter.py` | Calling an OpenAI-compatible provider (OpenRouter) through LangChain |
| 03 | `03_structured_output.py` | Prompt templates + `with_structured_output` to get a typed Pydantic object back |
| 04 | `04_agent_with_tool.py` | A LangChain agent that decides when to call a Python `@tool` |
| 05 | `05_openai_function_calling.py` | The tool-calling loop written by hand with the OpenAI SDK — call model, run tool, send result back, repeat |
| 06 | `06_agent_conversation_memory.py` | Agent that carries message history across turns and prints each message / tool call |
| 07 | `07_mcp_tool_discovery.py` | Connecting to a real MCP server (`mcp-server-fetch`), discovering its tools at runtime and letting the model call them |
| 08 | `08_multi_tool_agent.py` | Agent choosing between several tools with persistent chat history |
| — | `chatbot/` | Small terminal chatbot split into an entry point and an LLM service module |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env     # add the keys for the providers you want to use
python 01_groq_chat.py
```

Run the chatbot with `cd chatbot && python main.py`. Type `exit` to quit the interactive scripts. Script 07 needs an OpenAI key and runs the `mcp-server-fetch` server locally.
