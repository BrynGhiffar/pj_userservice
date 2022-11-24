import aiohttp, os
from discord import Webhook
from dotenv import load_dotenv

def get_webhook() -> str:
    load_dotenv()
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if not WEBHOOK_URL:
        return "NO WEBHOOK"
    else:
        return WEBHOOK_URL