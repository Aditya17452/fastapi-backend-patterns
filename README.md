# FastAPI Backend Patterns

Two self-contained projects covering the backend and LLM fundamentals behind production AI services.

| Folder | What it covers |
|---|---|
| [`student-api/`](student-api) | FastAPI service with a layered architecture, JWT auth, Argon2 password hashing, Redis cache-aside with graceful fallback, PostgreSQL and Alembic migrations |
| [`llm-basics/`](llm-basics) | Step-by-step scripts from a raw LLM call to structured output, LangChain agents with tools, a hand-written function-calling loop and runtime tool discovery from an MCP server |

Each folder has its own README, `requirements.txt` and `.env.example`.

**Related:** [Expense_Tracker_MCP](https://github.com/Aditya17452/Expense_Tracker_MCP) — a FastAPI expense tracker that also exposes its features to AI assistants through an MCP server · [rag-document-qa](https://github.com/Aditya17452/rag-document-qa) — PDF ingestion and semantic search with Weaviate.

## Tech stack

Python · FastAPI · SQLAlchemy · Alembic · PostgreSQL · Redis · PyJWT · Groq · OpenAI · LangChain · MCP
