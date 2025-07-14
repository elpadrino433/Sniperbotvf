
import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import telegram
import json
import threading
import time
from flask import Flask

BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = '@tUl5IOp8c8dhM2Nh'
MONTREAL = pytz.timezone("America/Montreal")
DATA_FILE = 'data.json'

app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "Bot actif."

def fetch_matches(url, label):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    matches = []
    for row in soup.select('.table-main tr'):
        teams = row.select_one('.team-name')
        odds = row.select('.odds-nowrp')
        if teams and len(odds) >= 2:
            try:
                team_names = teams.get_text(strip=True)
                cote = float(odds[0].get_text(strip=True))
                if cote >= 1.5:
                    matches.append((label, team_names, cote))
            except:
                continue
    return matches

def get_today_signals():
    sports = [
        ("https://www.betexplorer.com/next/soccer/", "⚽ Foot"),
        ("https://www.betexplorer.com/baseball/usa/mlb/", "⚾ MLB"),
        ("https://www.betexplorer.com/basketball/usa/nba/", "🏀 NBA"),
        ("https://www.betexplorer.com/boxing/", "🥊 Boxe"),
    ]
    today = datetime.datetime.now(MONTREAL)
    if today.month >= 10 or today.month <= 4:
        sports.append(("https://www.betexplorer.com/hockey/usa/nhl/", "🏒 NHL"))

    all_matches = []
    for url, label in sports:
        all_matches.extend(fetch_matches(url, label))
    return all_matches

def save_signals(matches):
    today = datetime.datetime.now(MONTREAL).strftime("%Y-%m-%d")
    data = {"date": today, "matches": []}
    for label, teams, cote in matches:
        data["matches"].append({
            "label": label,
            "teams": teams,
            "cote": cote,
            "result": "pending"
        })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def send_signals():
    bot = telegram.Bot(token=BOT_TOKEN)
    matches = get_today_signals()
    if not matches:
        bot.send_message(chat_id=CHAT_ID, text="❌ Aucun signal aujourd’hui.
On reste patient.")
        return

    message = "🔥 Signaux du jour – CLUB SNIPER BANKS VIP 🔥\n\n"
    simples = matches[:2]
    combiné = matches[2:6]
    save_signals(simples + combiné)
    for label, teams, cote in simples:
        message += f"{label}\n💥 {teams}\n💰 Cote : {cote}\n🧠 Confiance : {round(min(cote / 2, 0.85)*100)} %\n💸 Mise : 2 %\n\n"

    if combiné:
        total = 1
        message += "🔥 Combiné 🔥\n"
        for label, teams, cote in combiné:
            message += f"{label} – {teams} – {cote}\n"
            total *= cote
        message += f"💰 Total combiné : {round(total, 2)}\n🧠 Confiance : 76 %\n💸 Mise : 1.5 %"

    bot.send_message(chat_id=CHAT_ID, text=message)

def auto_trigger_loop():
    while True:
        now = datetime.datetime.now(MONTREAL)
        if now.hour == 11 and now.minute == 30:
            send_signals()
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=auto_trigger_loop).start()
    app.run(host="0.0.0.0", port=10000)
