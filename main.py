import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import json
import threading
import time
import os
import asyncio
from flask import Flask
from telegram import Bot
from telegram.request import HTTPXRequest

# === CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "TON_TOKEN_ICI")  # Change manuellement si tu ne veux pas utiliser Render env var
CHAT_ID = int(os.getenv("CHAT_ID", "-1002840077042"))  # Change aussi ici si besoin
MONTREAL = pytz.timezone("America/Montreal")
HISTORIQUE_FILE = 'historique.json'

request = HTTPXRequest(pool_timeout=30.0)
bot = Bot(token=BOT_TOKEN, request=request)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot SNIPER actif."

def fetch_matches(url, label):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
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
    except Exception as e:
        print(f"[ERREUR] fetch_matches: {e}")
        return []

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
    historique = []

    if os.path.exists(HISTORIQUE_FILE):
        with open(HISTORIQUE_FILE, 'r') as f:
            historique = json.load(f)

    for label, teams, cote in matches:
        historique.append({
            "date": today,
            "label": label,
            "teams": teams,
            "cote": cote,
            "result": "pending"
        })

    with open(HISTORIQUE_FILE, 'w') as f:
        json.dump(historique, f)

async def send_signals():
    matches = get_today_signals()
    if not matches:
        await bot.send_message(chat_id=CHAT_ID, text="❌ Aucun signal aujourd’hui. On reste patient.")
        return

    message = "🔥 Signaux du jour – CLUB SNIPER BANKS VIP 🔥\n\n"
    simples = matches[:2]
    combiné = matches[2:6]
    save_signals(simples + combiné)

    for label, teams, cote in simples:
        try:
            team1, team2 = teams.split("–")
            equipe_jouee = team1.strip()
        except:
            equipe_jouee = teams.strip()

        message += (
            f"{label}\n"
            f"💥 Match : {teams}\n"
            f"🎯 Équipe à jouer : {equipe_jouee}\n"
            f"💰 Cote : {cote}\n"
            f"🧠 Confiance : {round(min(cote / 2, 0.85) * 100)} %\n"
            f"💸 Mise : 2 %\n\n"
        )

    if combiné:
        total = 1
        message += "🔥 Combiné 🔥\n"
        for label, teams, cote in combiné:
            try:
                team1, team2 = teams.split("–")
                equipe_jouee = team1.strip()
            except:
                equipe_jouee = teams.strip()
            message += f"{label}\n🎯 {teams} – Équipe à jouer : {equipe_jouee} – Cote : {cote}\n"
            total *= cote
        message += f"\n💰 Total combiné : {round(total, 2)}\n🧠 Confiance : 76 %\n💸 Mise : 1.5 %"

    await bot.send_message(chat_id=CHAT_ID, text=message)

@app.route('/forcer-signal')
def forcer_signal():
    asyncio.run(send_signals())
    return "✅ Signal forcé envoyé."

@app.route('/test-signal')
def test_signal():
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot SNIPER."))
    return "✅ Message test envoyé."

# === LANCEMENT PRINCIPAL ===
if __name__ == "__main__":
    # Lancer signal test puis vrai signal
    try:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Le bot est actif et connecté !"))
        asyncio.run(send_signals())
    except Exception as e:
        print(f"[ERREUR démarrage] {e}")

    # Lancer serveur
    app.run(host="0.0.0.0", port=10000)
