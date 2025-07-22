# Configuration file for Telegram CC Checker Bot
import os

# Telegram Bot Configuration
# For Render.com deployment, use environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN", "7871173816:AAEkTTCRHnqxi8JJy-Kx9mwzYlq3lwKxQAo")

# Bot Settings
MAX_CARDS_PER_MASS_CHECK = int(os.getenv("MAX_CARDS_PER_MASS_CHECK", "0"))  # 0 = unlimited
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "4000"))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "5"))

# Rate Limiting (optional - to avoid being rate limited)
DELAY_BETWEEN_CHECKS = float(os.getenv("DELAY_BETWEEN_CHECKS", "0.5"))
MAX_CONCURRENT_CHECKS = int(os.getenv("MAX_CONCURRENT_CHECKS", "10"))

# Render.com specific settings
PORT = int(os.getenv("PORT", "10000"))
ENVIRONMENT = os.getenv("RENDER", "development")
