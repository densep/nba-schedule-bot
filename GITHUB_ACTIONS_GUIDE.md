# GitHub Actions Setup for NBA Bot

## Overview
GitHub Actions can run your NBA schedule bot in the cloud, so it works even when your laptop is closed.

## Free Tier Limits
- **Private repos**: 2,000 minutes/month (plenty for daily runs)
- **Public repos**: Unlimited minutes
- **Each run**: ~1-2 minutes = ~60 runs/month for private repos

## Pros
✅ Runs in cloud (laptop can be off)
✅ Free for your use case
✅ Reliable scheduled runs
✅ No server maintenance

## Cons
⚠️ Need to store bot in GitHub repo
⚠️ Warning bot needs different approach (can't run 24/7)
⚠️ Secrets stored in GitHub (secure but less private than local)

## Setup Steps

1. **Create GitHub repo** (public or private)
2. **Upload bot code** to repo
3. **Add secrets** in repo settings:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. **Create workflow file** (`.github/workflows/nba_bot.yml`)
5. **Schedule runs** using cron syntax

## Example Workflow File

See `.github/workflows/nba_bot.yml` for the full setup.

## Warning Bot Limitation

The warning bot needs to run continuously (checks every minute), which GitHub Actions can't do efficiently. Better options:
- Keep laptop awake (caffeinate)
- Use a Raspberry Pi
- Use a cloud server (AWS EC2, DigitalOcean)

## Recommended Setup

**Morning Schedule Bot**: ✅ Use GitHub Actions (runs once daily)
**Warning Bot**: ❌ Use laptop/always-on device (needs continuous monitoring)


