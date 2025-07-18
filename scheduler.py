import schedule
import time
from telegram_bot import send_daily_picks, send_weekly_report

def schedule_daily_tasks():
    schedule.every().day.at("11:00").do(send_daily_picks)
    schedule.every().sunday.at("17:00").do(send_weekly_report)

    while True:
        schedule.run_pending()
        time.sleep(1)