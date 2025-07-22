#!/usr/bin/env python3
"""
Health check script for Render.com deployment
This script can be used to verify the bot is running correctly
"""

import asyncio
import aiohttp
import os
from config import BOT_TOKEN

async def check_bot_health():
    """Check if the bot is responsive"""
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Bot token not configured")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            # Check Telegram Bot API
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        bot_info = data.get("result", {})
                        print(f"✅ Bot is healthy: @{bot_info.get('username', 'unknown')}")
                        return True
                    else:
                        print(f"❌ Bot API error: {data}")
                        return False
                else:
                    print(f"❌ HTTP error: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(check_bot_health())
    exit(0 if result else 1)
