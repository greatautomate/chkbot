# Render.com Deployment Guide

This guide will help you deploy the Telegram CC Checker Bot on Render.com as a background worker.

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render.com Account** - Sign up at [render.com](https://render.com)
3. **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather)

## Step-by-Step Deployment

### 1. Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/telegram-cc-bot.git
   git push -u origin main
   ```

### 2. Deploy on Render.com

1. **Login to Render.com** and go to your dashboard

2. **Create New Service**:
   - Click "New +" → "Background Worker"
   - Connect your GitHub repository
   - Select the repository containing your bot

3. **Configure Service**:
   - **Name**: `telegram-cc-bot` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python telegram_cc_bot.py`
   - **Plan**: Free (or paid for better performance)

4. **Set Environment Variables**:
   - Click "Environment" tab
   - Add the following variables:
     ```
     BOT_TOKEN = your_actual_bot_token_here
     MAX_CARDS_PER_MASS_CHECK = 0
     DELAY_BETWEEN_CHECKS = 0.5
     ```

5. **Deploy**:
   - Click "Create Background Worker"
   - Wait for deployment to complete

### 3. Verify Deployment

1. **Check Logs**:
   - Go to your service dashboard
   - Click "Logs" tab
   - Look for "✅ Bot handlers registered successfully"

2. **Test Bot**:
   - Message your bot on Telegram
   - Try `/start` command
   - Verify it responds correctly

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | - | ✅ Yes |
| `MAX_CARDS_PER_MASS_CHECK` | Max cards per mass check (0 = unlimited) | 0 | No |
| `DELAY_BETWEEN_CHECKS` | Delay between checks (seconds) | 0.5 | No |
| `MAX_CONCURRENT_CHECKS` | Max concurrent checks | 10 | No |

## Render.com Configuration Files

- **`render.yaml`** - Service configuration (optional)
- **`runtime.txt`** - Python version specification
- **`Procfile`** - Process definition
- **`requirements.txt`** - Python dependencies

## Monitoring and Maintenance

### Viewing Logs
```bash
# Access logs through Render dashboard or CLI
render logs -s your-service-name
```

### Health Check
The bot includes automatic health monitoring. Check the logs for:
- `✅ Bot handlers registered successfully`
- `🚀 Starting polling...`

### Troubleshooting

**Bot not responding:**
1. Check environment variables are set correctly
2. Verify bot token is valid
3. Check logs for error messages

**Deployment fails:**
1. Ensure all files are committed to GitHub
2. Check requirements.txt is present
3. Verify Python version compatibility

**Rate limiting issues:**
1. Increase `DELAY_BETWEEN_CHECKS`
2. Set `MAX_CARDS_PER_MASS_CHECK` to a lower number (default is unlimited)

## Scaling and Performance

### Free Tier Limitations
- 750 hours/month runtime
- Sleeps after 15 minutes of inactivity
- Limited CPU and memory

### Upgrading
For production use, consider upgrading to a paid plan for:
- 24/7 uptime
- Better performance
- More resources

## Security Best Practices

1. **Never commit bot tokens** to your repository
2. **Use environment variables** for sensitive data
3. **Regularly rotate** your bot token
4. **Monitor logs** for suspicious activity

## Auto-Deployment

To enable automatic deployment on code changes:
1. Go to service settings
2. Enable "Auto-Deploy"
3. Select branch (usually `main`)

Now your bot will automatically redeploy when you push changes to GitHub!

## Support

If you encounter issues:
1. Check Render.com documentation
2. Review bot logs for errors
3. Verify Telegram Bot API status
4. Test locally before deploying
