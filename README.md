# Telegram CC Checker Bot

A Telegram bot for checking credit cards converted from the original charge.py script.

## Features

- **Single Check** (`/chk`): Check individual credit cards
- **Mass Check** (`/mass`): Check multiple credit cards at once
- **File Check**: Upload .txt files with credit cards (only shows hits)

## 🌐 Render.com Deployment

Deploy as a 24/7 background worker on Render.com's free tier:

### Quick Steps:
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Telegram CC Checker Bot"
   git remote add origin https://github.com/yourusername/telegram-cc-bot.git
   git push -u origin main
   ```

2. **Deploy on Render.com**:
   - Go to [render.com](https://render.com)
   - Create new "Background Worker"
   - Connect your GitHub repository
   - Set environment variable: `BOT_TOKEN = your_bot_token_here`
   - Deploy!

📖 **Detailed Guide**: See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## Usage

### Commands

- `/start` - Show welcome message and available commands
- `/chk <cc|mm|yyyy|cvv>` - Check a single credit card
- `/mass <cards>` - Check multiple cards (unlimited, separate with spaces)

### Usage Examples

**Single Check:**
```
/chk 1234567890123456|12|2025|123
```

**Mass Check:**
```
/mass 1234567890123456|12|2025|123 4111111111111111|01|2026|456
```

**File Upload:**
- Send a `.txt` file containing credit cards (one per line)
- The bot will only return hits (successful charges)
- **No limit on file size or number of cards**
- Example file content:
```
1234567890123456|12|2025|123
4111111111111111|01|2026|456
5555555555554444|03|2027|789
```

### Card Format

All cards must be in the format: `cc|mm|yyyy|cvv`

Examples:
- `1234567890123456|12|2025|123`
- `4111111111111111|01|2026|456`
- `5555555555554444|03|2027|789`

## Features

1. **Telegram Integration**: Works as a Telegram bot
2. **Unlimited Cards**: No limits on number of cards to check
3. **File Handling**: .txt files only show hits, while /chk and /mass show all responses
4. **Better Formatting**: Results include emojis and better formatting for Telegram
5. **Cloud Ready**: Optimized for Render.com deployment
6. **24/7 Operation**: Runs continuously as a background worker

## Environment Variables

For Render.com deployment, configure these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram bot token | ✅ Yes |
| `MAX_CARDS_PER_MASS_CHECK` | Max cards per batch (0 = unlimited) | No (0) |
| `DELAY_BETWEEN_CHECKS` | Rate limiting delay | No (0.5s) |

## Security Note

⚠️ **Important**: This bot is for educational purposes only. Make sure to:
- Keep your bot token secure
- Use responsibly and legally
- Consider the ethical implications of credit card testing

## Troubleshooting

- If the bot doesn't respond, check your bot token
- Ensure all dependencies are installed
- Check that the bot has proper permissions in your Telegram chat
