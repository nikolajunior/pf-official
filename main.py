import discord
from datetime import datetime, timezone      # ← Added timezone here
import os
import requests

# No intents needed for selfbots in discord.py-self

client = discord.Client(self_bot=True)  # Explicit self-bot mode

webhook_url = os.getenv("WEBHOOK_URL")

def send_webhook_message(content):
    if not webhook_url:
        print("Webhook URL is missing – set WEBHOOK_URL env var")
        return
    
    try:
        data = {"content": content}
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"Webhook failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending webhook: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('Selfbot is ready.')
    
    # Removed invalid accept_invite call – no such method exists.
    # If you want to accept invites automatically, implement proper logic here
    # (e.g., monitor DMs or use on_invite_create if supported).

@client.event
async def on_member_join(member):
    try:
        guild = member.guild
        # Fixed: Use timezone-aware UTC now to match member.created_at
        account_age = (datetime.now(timezone.utc) - member.created_at).days
        
        message = (
            f"📥 **New Join Detected**\n"
            f"Server: **{guild.name}**\n"
            f"User: {member.name} ({member})\n"
            f"User ID: {member.id}\n"
            f"Account Age: {account_age} days"
        )
        
        send_webhook_message(message)
        print(f"Sent webhook for join: {member.name}")
    except Exception as e:
        print(f"Error in on_member_join: {e}")

# Load token from environment (set in Railway Variables)
user_token = os.environ.get("DISCORD_TOKEN")
if not user_token:
    print("DISCORD_TOKEN environment variable is missing!")
    raise ValueError("DISCORD_TOKEN is required")

print("Starting selfbot...")
client.run(user_token)
