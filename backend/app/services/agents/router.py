from pydantic import BaseModel, Field
import json
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

class RouteDecision(BaseModel):
    agent: str = Field(description="The assigned agent: 'sales', 'support', 'analytics', or 'general'.")
    confidence: float = Field(description="Confidence level between 0.0 and 1.0")

async def route_query(user_message: str) -> str:
    prompt = f"""You are a Router Agent for a real estate company.
Classify the user's message into one of these categories:
- 'sales': User is looking for properties, asking about prices, features, or EMI calculations.
- 'support': User is asking to book a site visit, report an issue, or create a support ticket.
- 'analytics': Admin user asking for system statistics, summary, performance, users count, or data insights.
- 'general': Greetings, casual talk, or queries that don't fit the above.

User message: "{user_message}"

Respond strictly in JSON matching this schema:
{{
  "agent": "sales" | "support" | "analytics" | "general",
  "confidence": 0.95
}}
"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("agent", "general")
    except:
        return "general"
