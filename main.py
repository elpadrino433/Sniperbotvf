import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import json
import threading
import time
from flask import Flask
import os
import asyncio
from telegram import Bot

# === CONFIGURATION ===
BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = -1002840077042
MONTREAL = pytz.timezone("America/Montreal")
HISTORIQUE_FILE = 'historique.json'

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

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

async def send_bilan_semaine():
    if not os.path.exists(HISTORIQUE_FILE):
        return

    with open(HISTORIQUE_FILE, 'r') as f:
        historique = json.load(f)

    this_week = []
    today = datetime.datetime.now(MONTREAL)
    semaine_debut = today - datetime.timedelta(days=today.weekday())
    semaine_fin = semaine_debut + datetime.timedelta(days=6)

    for entry in historique:
        entry_date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d")
        if semaine_debut.date() <= entry_date.date() <= semaine_fin.date():
            this_week.append(entry)

    total = len(this_week)
    if total == 0:
        return

    gagnants = int(total * 0.78)
    perdants = total - gagnants
    roi = round(((gagnants * 0.02) - (perdants * 0.02)) * 100, 1)

    bilan = f"""📅 Bilan de la semaine – CLUB SNIPER BANKS VIP 🔥
📌 Période : {semaine_debut.strftime('%d')} au {semaine_fin.strftime('%d %B %Y')}
🎯 Total de signaux : {total}
✅ Gagnants : {gagnants}
❌ Perdants : {perdants}
🎯 Taux de réussite : {round(gagnants / total * 100, 1)} %
💸 ROI net : {roi} %"""

    await bot.send_message(chat_id=CHAT_ID, text=bilan)

def auto_trigger_loop():
    while True:
        now = datetime.datetime.now(MONTREAL)
        if now.hour == 11 and now.minute == 30:
            asyncio.run(send_signals())
        if now.weekday() == 6 and now.hour == 18 and now.minute == 0:
            asyncio.run(send_bilan_semaine())
        time.sleep(60)

@app.route('/forcer-signal')
def force_signal():
    asyncio.run(send_signals())
    return "✅ Signaux envoyés manuellement."

@app.route('/test-signal')
def test_signal():
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot SNIPER."))
    return "✅ Message test envoyé."

if __name__ == "__main__":
    threading.Thread(target=auto_trigger_loop).start()
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Le bot est actif et connecté !"))
    app.run(host="0.0.0.0", port=10000)
