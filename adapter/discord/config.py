import aiohttp, os
from discord import Webhook
from dotenv import load_dotenv

def get_webhook() -> str:
    load_dotenv()
    return os.getenv("WEBHOOK_URL")