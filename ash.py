import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file
load_dotenv()

# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY was not found. "
        "Add it to your .env file."
    )

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


def chat(message, history):
    messages = []

    # Add previous conversation
    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content", "")

            if role in ["user", "assistant"]:
                messages.append({
                    "role": role,
                    "content": content
                })

        # Support older Gradio history format
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_message, assistant_message = item

            if user_message:
                messages.append({
                    "role": "user",
                    "content": user_message
                })

            if assistant_message:
                messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })

    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


app = gr.ChatInterface(
    fn=chat,
    title="🤖 My AI Chatbot",
    description="Chat with my AI assistant!"
)

app.launch()