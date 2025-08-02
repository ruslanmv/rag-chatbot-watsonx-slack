from ibm_watsonx_orchestrate.agent_builder.tools import tool
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import threading
import time

@tool
def start_slack_bot(bot_token: str, app_token: str, agent_name: str = "rag_chatbot") -> str:
    """
    Start the Slack bot to listen for messages and respond using the RAG agent
    
    Args:
        bot_token: Slack bot token (xoxb-...)
        app_token: Slack app token (xapp-...)
        agent_name: Name of the agent to use for responses
    
    Returns:
        Status message
    """
    
    app = App(token=bot_token)
    
    @app.event("app_mention")
    def handle_app_mention_events(body, say, client):
        try:
            user_message = body["event"]["text"]
            # Remove bot mention from message
            bot_user_id = body["authorizations"][0]["user_id"]
            cleaned_message = user_message.replace(f"<@{bot_user_id}>", "").strip()
            
            # Here you would call your RAG agent
            # For now, we'll return a placeholder response
            response = f"RAG Bot received: {cleaned_message}"
            
            say(response)
            
        except Exception as e:
            say(f"Sorry, I encountered an error: {str(e)}")
    
    @app.event("message")
    def handle_direct_messages(body, say, client):
        try:
            if body["event"]["channel_type"] == "im":
                user_message = body["event"]["text"]
                
                # Process with RAG agent
                response = f"RAG Bot received DM: {user_message}"
                
                say(response)
                
        except Exception as e:
            say(f"Sorry, I encountered an error: {str(e)}")
    
    # Start the bot in a separate thread
    def run_bot():
        handler = SocketModeHandler(app, app_token)
        handler.start()
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    return "Slack bot started successfully!"

@tool
def send_slack_message(channel: str, message: str, bot_token: str) -> str:
    """
    Send a message to a Slack channel
    
    Args:
        channel: Slack channel ID or name
        message: Message to send
        bot_token: Slack bot token
    
    Returns:
        Status message
    """
    from slack_sdk import WebClient
    
    client = WebClient(token=bot_token)
    
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        return f"Message sent successfully to {channel}"
    except Exception as e:
        return f"Error sending message: {str(e)}"
