import json
from openai import AsyncOpenAI
from typing import List, Dict, Any
from app.services.tools import search_properties, calculate_emi, book_site_visit, create_support_ticket, get_analytics_summary_tool
from app.db.session import SessionLocal
from app.services.agents.router import route_query
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

class LLMService:
    def __init__(self, model: str = None):
        self.model = model or settings.OPENAI_MODEL
        self.client = client
        
    async def chat(self, messages: List[Dict[str, Any]], user_id: int) -> str:
        last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        agent_type = await route_query(last_user_msg)
        
        tools = []
        system_prompt = "You are a general Real Estate AI assistant."
        
        if agent_type == "sales":
            system_prompt = "You are an expert Real Estate Sales Agent. Help users find properties and calculate EMIs. Be persuasive and helpful."
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "search_properties",
                        "description": "Search for properties in the database.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string"},
                                "min_price": {"type": "number"},
                                "max_price": {"type": "number"},
                                "property_type": {"type": "string"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "calculate_emi",
                        "description": "Calculate the EMI (Equated Monthly Installment) for a property loan.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "principal": {"type": "number"},
                                "rate": {"type": "number"},
                                "years": {"type": "integer"}
                            },
                            "required": ["principal", "rate", "years"]
                        }
                    }
                }
            ]
        elif agent_type == "support":
            system_prompt = "You are a Real Estate Support Agent. Help users book site visits and resolve issues by logging support tickets. For dates, assume ISO formats."
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "book_site_visit",
                        "description": "Book a site visit for a property. Use ISO datetime string.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "property_id": {"type": "integer"},
                                "scheduled_at": {"type": "string", "description": "ISO format date time string"}
                            },
                            "required": ["property_id", "scheduled_at"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "create_support_ticket",
                        "description": "Create a support ticket for the customer.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "subject": {"type": "string"},
                                "description": {"type": "string"},
                                "category": {"type": "string"}
                            },
                            "required": ["subject", "description"]
                        }
                    }
                }
            ]
        elif agent_type == "analytics":
            system_prompt = "You are a Real Estate Data & Analytics Agent. You help administrators understand platform performance. You can fetch system analytics and summarize them effectively."
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_analytics_summary_tool",
                        "description": "Get the overall analytics summary of the platform including properties, users, visits, and support requests.",
                        "parameters": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                }
            ]
            
        if messages and messages[0]["role"] == "system":
            messages[0]["content"] += " " + system_prompt
        else:
            messages.insert(0, {"role": "system", "content": system_prompt})
            
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
                
            response = await self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            
            if hasattr(message, "tool_calls") and message.tool_calls:
                db = SessionLocal()
                try:
                    messages.append(message)
                    for tool_call in message.tool_calls:
                        args = json.loads(tool_call.function.arguments)
                        
                        tool_name = tool_call.function.name
                        res = "Unknown tool"
                        if tool_name == "calculate_emi":
                            res = str(calculate_emi(**args))
                        elif tool_name == "search_properties":
                            res = json.dumps(search_properties(db, **args))
                        elif tool_name == "book_site_visit":
                            res = book_site_visit(db, customer_id=user_id, **args)
                        elif tool_name == "create_support_ticket":
                            res = create_support_ticket(db, customer_id=user_id, **args)
                        elif tool_name == "get_analytics_summary_tool":
                            res = get_analytics_summary_tool(db)
                            
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": res
                        })
                    
                    second_response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages
                    )
                    return second_response.choices[0].message.content or ""
                finally:
                    db.close()
            else:
                return message.content or ""
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm sorry, I'm having trouble connecting to my AI brain right now."
