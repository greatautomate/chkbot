# Project Structure

## Essential Files for Render.com Deployment

```
telegram-cc-bot/
├── telegram_cc_bot.py      # Main bot application
├── config.py               # Configuration with environment variables
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version specification
├── Procfile               # Render.com process definition
├── render.yaml            # Render.com service configuration
├── health_check.py        # Health monitoring script
├── README.md              # Project documentation
├── RENDER_DEPLOYMENT.md   # Detailed deployment guide
└── .gitignore            # Git ignore rules
```

## File Descriptions

- **`telegram_cc_bot.py`** - The main Telegram bot with unlimited card checking
- **`config.py`** - Configuration that reads from environment variables
- **`requirements.txt`** - Python packages needed (aiohttp, fake-useragent, python-telegram-bot)
- **`runtime.txt`** - Specifies Python 3.11.0 for Render.com
- **`Procfile`** - Tells Render.com how to run the bot as a background worker
- **`render.yaml`** - Optional service configuration for Render.com
- **`health_check.py`** - Script to verify bot health and connectivity

## Ready for Deployment

All files are optimized for Render.com deployment. Simply:
1. Push to GitHub
2. Create Background Worker on Render.com
3. Set BOT_TOKEN environment variable
4. Deploy!
