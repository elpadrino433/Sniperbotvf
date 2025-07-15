import datetime
import pytz
import requests
import json
import threading
import time
import os
import asyncio
from flask import Flask
from telegram import Bot

# === CONFIGURATION ===
BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = -1002840077042
MONTREAL = pytz.timezone("America/Montreal")
API_KEY = "911564e0596507ce7da914fd806bde9f"  # ← ta clé API Sports
HISTORIQUE_FILE = 'historique.json'

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route('/')
def keep_alive():
    return "Bot actif."

def fetch_matches_api_sports(sport="football", count=5):
    headers = {
        "x-apisports-key": API_KEY
    }

    if sport == "football":
        url = f"https://v3.football.api-sports.io/fixtures?next={count}"
    else:
        return []

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        matches = []

        for match in r.json()["response"]:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            date = match["fixture"]["date"]
            match_str = f"{home} – {away}"
            fake_cote = 1.60  # Valeur provisoire
            matches.append(("⚽ Foot", match_str, fake_cote))

        return matches
    except Exception as e:
        print("Erreur API:", e)
        return []

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
    matches = fetch_matches_api_sports("football", count=5)
    if not matches:
        await bot.send_message(chat_id=CHAT_ID, text="❌ Aucun signal aujourd’hui. On reste patient.") 
        return

    message = "🔥 Signaux du jour – CLUB SNIPER BANKS VIP 🔥\n\n"
    simples = matches[:2]
    combiné = matches[2:5]
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
def force_signal():
    asyncio.run(send_signals())
    return "✅ Signaux envoyés manuellement."

@app.route('/test-signal')
def test_signal():
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot SNIPER."))
    return "✅ Message test envoyé."

def auto_trigger_loop():
    while True:
        now = datetime.datetime.now(MONTREAL)
        if now.hour == 11 and now.minute == 30:
            asyncio.run(send_signals())
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=auto_trigger_loop).start()
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Le bot est actif et connecté !"))
    app.run(host="0.0.0.0", port=10000)
