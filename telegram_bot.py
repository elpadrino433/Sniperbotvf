import os
import telegram
from dotenv import load_dotenv
from analyzer import analyze_today_matches, get_weekly_summary

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
bot = telegram.Bot(token=TOKEN)

def send_daily_picks():
    picks = analyze_today_matches()
    if picks:
        message = "\n".join(picks)
    else:
        message = "Aucun match fiable aujourd'hui. \U0001F914"
    bot.send_message(chat_id=GROUP_ID, text=message)

def send_weekly_report():
    summary = get_weekly_summary()
    bot.send_message(chat_id=GROUP_ID, text=summary)