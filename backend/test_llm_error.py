import asyncio
import os
from app.services.llm import LLMService

async def main():
    service = LLMService()
    messages = [{"role": "user", "content": "I want to book a site visit for property ID 5 tomorrow at 3 PM."}]
    reply = await service.chat(messages, user_id=1)
    print("Reply:", reply)

if __name__ == "__main__":
    asyncio.run(main())
