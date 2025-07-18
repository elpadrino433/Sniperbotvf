import os
import time
import requests
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erreur: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def scan_and_notify():
    print("Scan en cours...")
    signal_present = False
    # Simule une absence de signal
    if not signal_present:
        send_telegram_message("⚠️ Aucun signal détecté depuis 14h.")
    else:
        print("Signal détecté")

if __name__ == "__main__":
    keep_alive()
    while True:
        scan_and_notify()
        time.sleep(3600)
