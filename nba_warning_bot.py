#!/usr/bin/env python3
"""
NBA Warning Bot
Monitors NBA games and sends warning messages 15 minutes before the 2nd to last game,
and a check-in message at the exact start time of the 2nd to last game.
"""

import requests
from datetime import datetime, timedelta
from telegram import Bot
import pytz
import os
import asyncio
import time
import sys

# Import from main bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nba_schedule_bot import BOT_TOKEN, CHAT_ID, TIMEZONE, ESPN_API_URL, send_message_async, normalize_team_abbrev

# Configuration
WARNING_MESSAGE = "15 min warning until overnight check"
CHECKIN_MESSAGE = "Hey! Checking in on if we should expect overnights tonight. Let me know and I can ready our in person bettor."
CHECKED_IN_FILE = "/Users/joey/nba-schedule-bot/last_checked_in.txt"


def get_today_games_with_times():
    """
    Fetches today's NBA games from ESPN API with their start times.
    
    Returns:
        List of tuples (game_datetime, team_matchup) sorted by time
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
                    team_matchup = away_team or home_team or "Unknown"
                else:
                    team_matchup = event.get("shortName", event.get("name", "Unknown"))
                
                games.append((local_time, team_matchup))
            except (ValueError, AttributeError) as e:
                continue

        # Sort by time
        games.sort(key=lambda x: x[0])
        return games
            
    except requests.RequestException as e:
        print(f"Error fetching schedule: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def get_second_to_last_game_time(games):
    """
    Gets the start time of the 2nd to last game.
    
    Args:
        games: List of tuples (game_datetime, team_matchup) sorted by time
        
    Returns:
        Tuple (game_datetime, team_matchup) or None if there aren't at least 2 games
    """
    if len(games) < 2:
        return None
    return games[-2]


def check_and_send_warning():
    """
    Checks if it's 15 minutes before the 2nd to last game and sends warning.
    Returns True if warning was sent.
    """
    arizona_tz = pytz.timezone(TIMEZONE)
    now = datetime.now(arizona_tz)
    
    games = get_today_games_with_times()
    if not games:
        return False
    
    second_to_last = get_second_to_last_game_time(games)
    if not second_to_last:
        return False
    
    game_time, team_matchup = second_to_last
    warning_time = game_time - timedelta(minutes=15)
    
    # Check if current time is within 1 minute of warning time
    time_diff = abs((now - warning_time).total_seconds())
    if time_diff <= 60:  # Within 1 minute
        # Check if we already sent this warning today
        warning_file = f"/Users/joey/nba-schedule-bot/warning_sent_{now.date()}.txt"
        if os.path.exists(warning_file):
            return False
        
        # Send warning
        message = WARNING_MESSAGE
        if asyncio.run(send_message_async(message)):
            # Mark as sent
            with open(warning_file, 'w') as f:
                f.write(str(now))
            print(f"✅ Warning sent at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            return True
    
    return False


def check_and_send_checkin():
    """
    Checks if it's exactly the start time of the 2nd to last game and sends check-in message.
    Returns True if check-in was sent.
    """
    arizona_tz = pytz.timezone(TIMEZONE)
    now = datetime.now(arizona_tz)
    
    games = get_today_games_with_times()
    if not games:
        return False
    
    second_to_last = get_second_to_last_game_time(games)
    if not second_to_last:
        return False
    
    game_time, team_matchup = second_to_last
    
    # Check if current time is within 1 minute of game start time
    time_diff = abs((now - game_time).total_seconds())
    if time_diff <= 60:  # Within 1 minute
        # Check if we already sent this check-in today
        checkin_file = f"/Users/joey/nba-schedule-bot/checkin_sent_{now.date()}.txt"
        if os.path.exists(checkin_file):
            return False
        
        # Send check-in
        message = CHECKIN_MESSAGE
        if asyncio.run(send_message_async(message)):
            # Mark as sent
            with open(checkin_file, 'w') as f:
                f.write(str(now))
            print(f"✅ Check-in sent at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            return True
    
    return False


def monitor_loop():
    """Main monitoring loop that checks every minute."""
    print("NBA Warning Bot started - Monitoring for 2nd to last game...")
    print("Checking every minute for warning (15 min before) and check-in times")
    
    while True:
        try:
            # Check for warning (15 min before)
            check_and_send_warning()
            
            # Check for check-in (exact game time)
            check_and_send_checkin()
            
            # Wait 1 minute before checking again
            time.sleep(60)
        except KeyboardInterrupt:
            print("\n⚠️  Monitoring stopped by user")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    monitor_loop()

