# NBA Schedule Telegram Bot

A Python bot that automatically fetches NBA game schedules from ESPN API and sends formatted messages to a Telegram chat.

## Features

- Fetches daily NBA game schedule from ESPN API
- Converts game times to Arizona time (MST/MDT)
- Sends beautifully formatted messages to Telegram
- Easy to schedule with cron or Task Scheduler

## Setup

### 1. Prerequisites

- Python 3.10 or newer
- Internet connection
- Telegram Bot Token (already configured)
- Telegram Chat ID (your chat ID or channel ID)

### 2. Installation

```bash
# Navigate to the project directory
cd nba-schedule-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

#### Get Telegram Chat ID

**For Personal Chat:**
1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start a conversation - it will show your Chat ID

**For Group/Channel:**
1. Add your bot to the group/channel as admin
2. Send a message in the group/channel
3. Visit: `https://api.telegram.org/bot8516534804:AAFvYFYmFBZi5Nkmi-c--C8YZYIHtL46s30/getUpdates`
4. Find the `chat.id` in the response

#### Set Chat ID

**Option A: Environment Variable (Recommended)**
```bash
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

**Option B: Edit Script Directly**
Edit `nba_schedule_bot.py` and replace:
- `CHAT_ID = "YOUR_CHAT_ID"` with your actual Chat ID

### 4. Test the Bot

```bash
python3 nba_schedule_bot.py
```

You should receive a message in your Telegram chat with today's NBA games.

## Automation

### macOS / Linux (Cron)

```bash
# Open crontab editor
crontab -e

# Add this line to run daily at 9:00 AM Arizona time
# Note: Adjust path to your script location
0 9 * * * /usr/bin/python3 /Users/joey/nba-schedule-bot/nba_schedule_bot.py >> /Users/joey/nba-schedule-bot/bot.log 2>&1
```

**Note:** Cron runs in system timezone. To run at 9:00 AM Arizona time regardless of server timezone, you may need to adjust the cron time based on your server's timezone.

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 09:00 AM
4. Set action: Start a program
   - Program: `python` (or full path to `python.exe`)
   - Arguments: `"C:\path\to\nba_schedule_bot.py"`
   - Start in: `C:\path\to\`

### Alternative: Python Script Scheduler

For more control, you can use the provided scheduler:

```bash
pip install schedule
python3 scheduler.py
```

This will run the bot continuously and execute it daily at 9:00 AM.

## Example Output

```
🏀 NBA Games Today (Nov 1, 2025):

Sacramento Kings @ Milwaukee Bucks — 2:00 PM MST
Minnesota Timberwolves @ Charlotte Hornets — 3:00 PM MST
Orlando Magic @ Washington Wizards — 4:00 PM MST
Golden State Warriors @ Indiana Pacers — 4:00 PM MST
Houston Rockets @ Boston Celtics — 5:00 PM MST
Dallas Mavericks @ Detroit Pistons — 7:00 PM MST
```

## Troubleshooting

### Bot doesn't send messages
- Verify CHAT_ID is correct
- Make sure you've started a conversation with your bot (for personal chats)
- Check that your bot has permission to send messages (for groups/channels)

### Timezone issues
- The script uses `America/Phoenix` timezone (MST/MDT)
- To change timezone, modify the `TIMEZONE` variable in the script

### API errors
- Check your internet connection
- ESPN API might be temporarily unavailable
- Verify the API URL is accessible

## Optional Enhancements

- Add estimated halftimes (+45 min & +60 min)
- Include live scores if games are ongoing
- Add Telegram commands like `/today`, `/tomorrow`, `/halftimes`
- Log results to a file or database
- Add error notifications

## License

Free to use and modify as needed.
