# GitHub Actions Setup - Step by Step

## ✅ Already Done
- ✅ Git repository initialized
- ✅ Code committed locally
- ✅ GitHub Actions workflow file created
- ✅ Sensitive files excluded from git

## Next Steps

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `nba-schedule-bot` (or any name you prefer)
3. Description: "Automated NBA schedule Telegram bot"
4. Choose **Public** (unlimited free Actions) or **Private** (2,000 min/month)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 2: Add Secrets to GitHub

1. Go to your new repository → **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add first secret:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token (get it from @BotFather on Telegram)
   - Click **Add secret**
5. Add second secret:
   - **Name**: `TELEGRAM_CHAT_ID`
   - **Value**: Your chat ID (see instructions below)
   - Click **Add secret**

### Step 3: Push Code to GitHub

**Option A: Using the script**
```bash
cd /Users/joey/nba-schedule-bot
./push_to_github.sh
```

**Option B: Manual push**
```bash
cd /Users/joey/nba-schedule-bot

# Replace YOUR_USERNAME and YOUR_REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 4: Verify It Works

1. Go to your GitHub repo → **Actions** tab
2. You should see "NBA Schedule Bot" workflow
3. To test immediately:
   - Click **Actions** → **NBA Schedule Bot**
   - Click **Run workflow** → **Run workflow**
   - Watch it run and check if message is sent!

### Step 5: Check Schedule

The bot will automatically run:
- **Daily at 9:00 AM Arizona time (MST)**
- Configured in `.github/workflows/nba_bot.yml` as `cron: '0 16 * * *'` (4:00 PM UTC)

## Troubleshooting

**"Repository not found"**
- Make sure you created the repo on GitHub first
- Check the repo name matches your command

**"Workflow failed"**
- Check **Actions** tab for error logs
- Verify secrets are set correctly
- Make sure you've started a conversation with your bot on Telegram

**"No messages received"**
- Check Actions logs for errors
- Verify bot token and chat ID in secrets
- Make sure you've sent /start to your bot

## What's Included

- `nba_schedule_bot_github.py` - Main bot (safe for GitHub, no hardcoded secrets)
- `.github/workflows/nba_bot.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies
- README files with documentation

## Notes

- The warning bot (`nba_warning_bot.py`) is included but still needs to run locally
- Secrets are stored securely in GitHub and never exposed
- Public repos get unlimited free Actions minutes


