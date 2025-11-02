# NBA Schedule Bot - GitHub Actions Setup

This bot automatically sends daily NBA game schedules via Telegram using GitHub Actions.

## Quick Setup

### 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name it (e.g., `nba-schedule-bot`)
4. Choose **Public** (unlimited free Actions) or **Private** (2,000 minutes/month)
5. Click "Create repository"

### 2. Add Repository Secrets

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:
   - **Name**: `TELEGRAM_BOT_TOKEN`
     **Value**: Your bot token (get it from @BotFather on Telegram)
   - **Name**: `TELEGRAM_CHAT_ID`
     **Value**: Your chat ID (see README.md for instructions on getting this)
4. Click **Add secret** for each

### 3. Push Code to GitHub

```bash
cd /Users/joey/nba-schedule-bot
git add .
git commit -m "Initial commit: NBA Schedule Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repo name.

### 4. Verify Workflow

1. Go to your repo → **Actions** tab
2. You should see "NBA Schedule Bot" workflow
3. It will run daily at 9:00 AM Arizona time
4. You can manually trigger it by going to **Actions** → **NBA Schedule Bot** → **Run workflow**

## Files Structure

- `nba_schedule_bot_github.py` - Main bot script (safe for GitHub, no hardcoded secrets)
- `.github/workflows/nba_bot.yml` - GitHub Actions workflow configuration
- `requirements.txt` - Python dependencies

## Schedule

The bot runs daily at:
- **9:00 AM MST** (Mountain Standard Time - Arizona time)
- Configured in `.github/workflows/nba_bot.yml` as `cron: '0 16 * * *'` (4:00 PM UTC)

## Testing

To test manually:
1. Go to **Actions** tab in your repo
2. Click **NBA Schedule Bot** workflow
3. Click **Run workflow** → **Run workflow**

## Troubleshooting

- **Bot not sending**: Check that secrets are set correctly
- **Workflow failing**: Check **Actions** tab for error logs
- **Time wrong**: Edit `.github/workflows/nba_bot.yml` and adjust the cron schedule

## Notes

- This setup is for the **morning schedule bot only**
- The **warning bot** still needs to run locally (requires continuous monitoring)
- All secrets are stored securely in GitHub and never exposed in logs


