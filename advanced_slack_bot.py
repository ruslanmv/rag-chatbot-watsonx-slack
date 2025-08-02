import os
import asyncio
import requests
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from ibm_watsonx_orchestrate.agent_builder.tools import tool

class SlackRAGBot:
    def __init__(self, bot_token, app_token, orchestrate_api_url="http://localhost:4321/api/v1"):
        self.app = AsyncApp(token=bot_token)
        self.app_token = app_token
        self.orchestrate_api_url = orchestrate_api_url
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.app.event("app_mention")
        async def handle_app_mention(body, say, client):
            await self.process_message(body, say, client, is_mention=True)
        
        @self.app.event("message")
        async def handle_direct_message(body, say, client):
            if body["event"]["channel_type"] == "im":
                await self.process_message(body, say, client, is_mention=False)
    
    async def process_message(self, body, say, client, is_mention=False):
        try:
            user_message = body["event"]["text"]
            
            if is_mention:
                # Remove bot mention
                bot_user_id = body["authorizations"][0]["user_id"]
                user_message = user_message.replace(f"<@{bot_user_id}>", "").strip()
            
            # Call watsonx Orchestrate agent
            response = await self.call_rag_agent(user_message)
            
            await say(response)
            
        except Exception as e:
            await say(f"Sorry, I encountered an error: {str(e)}")
    
    async def call_rag_agent(self, message):
        """Call the RAG agent via watsonx Orchestrate API"""
        try:
            # This would be the actual API call to your RAG agent
            payload = {
                "message": {
                    "role": "user",
                    "content": [{"response_type": "text", "text": message}]
                },
                "agent_id": "slack_rag_chatbot"
            }
            
            # For demo purposes, return a formatted response
            return f"🤖 RAG Bot Response:\n\nI received your question: '{message}'\n\nLet me search my knowledge base...\n\n[This would contain the actual RAG response from your knowledge base]"
            
        except Exception as e:
            return f"Error processing your request: {str(e)}"
    
    async def start(self):
        handler = AsyncSocketModeHandler(self.app, self.app_token)
        await handler.start_async()

@tool
def start_advanced_slack_bot(bot_token: str, app_token: str) -> str:
    """
    Start the advanced Slack RAG bot
    
    Args:
        bot_token: Slack bot token
        app_token: Slack app token
    
    Returns:
        Status message
    """
    bot = SlackRAGBot(bot_token, app_token)
    
    # Start bot in background
    import threading
    
    def run_bot():
        asyncio.run(bot.start())
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    return "Advanced Slack RAG bot started successfully!"
