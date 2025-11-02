#!/usr/bin/env python3
"""
NBA Schedule Telegram Bot (GitHub Actions Version)
Fetches NBA game schedule from ESPN API and sends formatted messages to Telegram.
This version uses environment variables for configuration (safe for GitHub).
"""

import requests
from datetime import datetime
from telegram import Bot
import pytz
import os
import asyncio


# Configuration - uses environment variables (set in GitHub Actions secrets)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TIMEZONE = "America/Phoenix"  # Arizona time (MST/MDT)
ESPN_API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"


def normalize_team_abbrev(abbrev: str) -> str:
    """
    Converts team abbreviation to 3-letter format.
    
    Args:
        abbrev: Team abbreviation from ESPN API
        
    Returns:
        3-letter abbreviation
    """
    if not abbrev:
        return abbrev
    
    abbrev = abbrev.upper()
    
    # Mapping of ESPN abbreviations to 3-letter abbreviations
    abbrev_map = {
        # Teams that need conversion
        "NO": "NOP",  # New Orleans Pelicans
        "SA": "SAS",  # San Antonio Spurs
        "NY": "NYK",  # New York Knicks
        "GS": "GSW",  # Golden State Warriors
        "UTAH": "UTA",  # Utah Jazz
    }
    
    # Check mapping first
    if abbrev in abbrev_map:
        return abbrev_map[abbrev]
    
    # If already 3 letters, return as is
    if len(abbrev) == 3:
        return abbrev
    
    # Handle longer abbreviations - take first 3 letters
    if len(abbrev) > 3:
        return abbrev[:3]
    
    # Handle shorter abbreviations - pad to 3 letters
    if len(abbrev) == 2:
        return abbrev + abbrev[-1]
    if len(abbrev) == 1:
        return abbrev + abbrev + abbrev
    
    return abbrev


def get_today_schedule() -> str:
    """
    Fetches today's NBA schedule from ESPN API and formats it.
    
    Returns:
        Formatted string with today's games or "No NBA games today 🏀"
    """
    try:
        # Get today's date in Arizona timezone
        arizona_tz = pytz.timezone(TIMEZONE)
        today = datetime.now(arizona_tz).date()
        
        # Fetch schedule from ESPN API
        response = requests.get(ESPN_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        games = []
        for event in data.get("events", []):
            # Parse and convert time
            event_date_str = event.get("date", "")
            if not event_date_str:
                continue
                
            # Handle ISO format date string
            if event_date_str.endswith("Z"):
                event_date_str = event_date_str.replace("Z", "+00:00")
            
            try:
                utc_time = datetime.fromisoformat(event_date_str)
                # Ensure UTC timezone
                if utc_time.tzinfo is None:
                    utc_time = pytz.UTC.localize(utc_time)
                
                # Convert to Arizona time
                local_time = utc_time.astimezone(arizona_tz)
                
                # Filter to only include today's games
                if local_time.date() != today:
                    continue
                
                # Extract team abbreviations from competitors
                away_team = None
                home_team = None
                competitions = event.get("competitions", [])
                if competitions:
                    competitors = competitions[0].get("competitors", [])
                    for competitor in competitors:
                        team = competitor.get("team", {})
                        abbreviation = team.get("abbreviation", "")
                        # Normalize to 3-letter abbreviation
                        abbreviation = normalize_team_abbrev(abbreviation)
                        if competitor.get("homeAway") == "away":
                            away_team = abbreviation
                        elif competitor.get("homeAway") == "home":
                            home_team = abbreviation
                
                # Format team names (away/home)
                if away_team and home_team:
                    team_matchup = f"{away_team}/{home_team}"
                elif away_team or home_team:
                    # Fallback if only one team is found
                    team_matchup = away_team or home_team or "Unknown"
                else:
                    # Fallback to event name if no teams found
                    team_matchup = event.get("shortName", event.get("name", "Unknown"))
                
                # Format time (handle both 12-hour and timezone abbreviation)
                game_time = local_time.strftime("%I:%M %p %Z").lstrip("0")
                
                games.append(f"{team_matchup} — {game_time}")
            except (ValueError, AttributeError) as e:
                event_name = event.get("name", "Unknown")
                print(f"Error parsing date for event {event_name}: {e}")
                continue

        if games:
            return "\n".join(games)
        else:
            return "No NBA games today 🏀"
            
    except requests.RequestException as e:
        return f"❌ Error fetching schedule: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


async def send_message_async(text: str) -> bool:
    """
    Sends a message to the specified Telegram chat (async).
    
    Args:
        text: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not BOT_TOKEN:
            print("❌ TELEGRAM_BOT_TOKEN is not set or is empty")
            return False
        
        bot = Bot(token=BOT_TOKEN)
        # Convert Chat ID to integer if it's a string
        chat_id = int(CHAT_ID) if isinstance(CHAT_ID, str) else CHAT_ID
        
        # Verify bot token first
        bot_info = await bot.get_me()
        
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            return True
        except Exception as send_error:
            error_msg = str(send_error)
            if "Unauthorized" in error_msg:
                print(f"❌ Unauthorized error. Possible causes:")
                print(f"   - Bot token is invalid or expired")
                print(f"   - Chat ID ({chat_id}) is incorrect")
                print(f"   - You haven't started a conversation with @{bot_info.username}")
                print(f"   → Go to Telegram and send /start to @{bot_info.username}")
            elif "Chat not found" in error_msg or "chat not found" in error_msg.lower():
                print(f"❌ Chat not found for chat ID: {chat_id}")
                print(f"   → Make sure you've started a conversation with @{bot_info.username}")
                print(f"   → Verify the TELEGRAM_CHAT_ID secret in GitHub Actions is correct")
            else:
                print(f"❌ Error sending Telegram message: {send_error}")
            return False
            
    except Exception as e:
        error_msg = str(e)
        if "Unauthorized" in error_msg:
            print(f"❌ Bot token is invalid or unauthorized")
            print(f"   → Verify TELEGRAM_BOT_TOKEN secret in GitHub Actions is correct")
        else:
            print(f"❌ Error initializing bot: {e}")
        return False


def send_message(text: str) -> bool:
    """
    Sends a message to the specified Telegram chat.
    
    Args:
        text: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    try:
        return asyncio.run(send_message_async(text))
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def main():
    """Main function to fetch schedule and send message."""
    # Validate configuration
    if not BOT_TOKEN or not CHAT_ID:
        error_msg = "⚠️  TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set as environment variables"
        print(error_msg)
        exit(1)
    
    # Get today's schedule
    schedule_text = get_today_schedule()
    
    # Check if schedule fetch failed
    if schedule_text.startswith("❌"):
        print(f"Error fetching schedule: {schedule_text}")
        exit(1)
    
    # Format final message
    arizona_tz = pytz.timezone(TIMEZONE)
    today_str = datetime.now(arizona_tz).strftime("%b %d, %Y")
    message = f"🏀 NBA Games Today ({today_str}):\n\n{schedule_text}"
    
    # Send message
    if send_message(message):
        print(f"✅ Message sent successfully at {datetime.now(arizona_tz).strftime('%Y-%m-%d %H:%M:%S %Z')}")
        exit(0)
    else:
        print("❌ Failed to send message")
        exit(1)


if __name__ == "__main__":
    main()


