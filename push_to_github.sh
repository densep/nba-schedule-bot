#!/bin/bash
# Script to push NBA Schedule Bot to GitHub

echo "🚀 NBA Schedule Bot - GitHub Push Script"
echo ""

# Check if remote is set
if ! git remote get-url origin &>/dev/null; then
    echo "⚠️  No GitHub remote configured yet."
    echo ""
    echo "First, create a repository on GitHub:"
    echo "1. Go to https://github.com/new"
    echo "2. Name it (e.g., 'nba-schedule-bot')"
    echo "3. Choose Public (unlimited Actions) or Private (2,000 min/month)"
    echo "4. Click 'Create repository'"
    echo ""
    read -p "Enter your GitHub username: " GITHUB_USER
    read -p "Enter your repository name: " REPO_NAME
    
    git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    echo ""
    echo "✅ Remote added!"
fi

echo ""
echo "📋 Next steps:"
echo "1. Add secrets to GitHub repo:"
echo "   - Go to Settings → Secrets and variables → Actions"
echo "   - Add TELEGRAM_BOT_TOKEN: (get from @BotFather on Telegram)"
echo "   - Add TELEGRAM_CHAT_ID: (see README.md for instructions)"
echo ""
read -p "Press Enter when secrets are added..."

echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Check your GitHub repo → Actions tab to see the workflow run."


