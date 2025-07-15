import datetime
import pytz
import requests
import json
import threading
import time
import asyncio
from flask import Flask
from telegram import Bot
from telegram.request import HTTPXRequest

# === CONFIGURATION ===
BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = -1002840077042
API_SPORTS_KEY = '911564e0596507ce7da914fd806bde9f'
ODDS_API_KEY = '660f7bbee0e51e9b4cc4701d4f0484fe'
MONTREAL = pytz.timezone("America/Montreal")
HISTORIQUE_FILE = 'historique.json'

# === INIT ===
request = HTTPXRequest(pool_timeout=30.0)
bot = Bot(token=BOT_TOKEN, request=request)
app = Flask(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# === ROUTES ===
@app.route('/')
def keep_alive():
    return "Bot actif."

@app.route('/test-signal')
def test_signal():
    loop.create_task(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot SNIPER."))
    return "✅ Test envoyé."

@app.route('/forcer-signal')
def force_signal():
    loop.create_task(send_signals())
    return "✅ Signaux envoyés manuellement."

# === LOGIQUE ===

def save_signals(matches):
    today = datetime.datetime.now(MONTREAL).strftime("%Y-%m-%d")
    historique = []

    if os.path.exists(HISTORIQUE_FILE):
        with open(HISTORIQUE_FILE, 'r') as f:
            historique = json.load(f)

    for match in matches:
        historique.append({
            "date": today,
            "sport": match['sport'],
            "teams": match['teams'],
            "cote": match['cote'],
            "result": "pending"
        })

    with open(HISTORIQUE_FILE, 'w') as f:
        json.dump(historique, f)

def fetch_from_apis():
    matches = []

    # FOOT (via API-SPORTS)
    headers = {
        'x-apisports-key': API_SPORTS_KEY
    }
    try:
        foot_data = requests.get("https://v3.football.api-sports.io/fixtures?next=5", headers=headers, timeout=10).json()
        for fixture in foot_data.get("response", []):
            teams = f"{fixture['teams']['home']['name']} – {fixture['teams']['away']['name']}"
            matches.append({
                "sport": "⚽ Foot",
                "teams": teams,
                "cote": 1.75  # Placeholder — vraie cote si tu veux la croiser
            })
    except Exception as e:
        print(f"[Foot API error] {e}")

    # Autres sports via The Odds API
    try:
        sports = [("basketball_nba", "🏀 NBA"), ("icehockey_nhl", "🏒 NHL"), ("baseball_mlb", "⚾ MLB"), ("boxing", "🥊 Boxe")]
        for key, emoji in sports:
            r = requests.get(
                f"https://api.the-odds-api.com/v4/sports/{key}/odds/?apiKey={ODDS_API_KEY}&regions=us&markets=h2h",
                timeout=10
            )
            data = r.json()
            for game in data[:2]:
                team_names = " – ".join(game["teams"])
                cote = game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
                if cote >= 1.5:
                    matches.append({
                        "sport": emoji,
                        "teams": team_names,
                        "cote": cote
                    })
    except Exception as e:
        print(f"[Odds API error] {e}")

    return matches

async def send_signals():
    matches = fetch_from_apis()
    if not matches:
        await bot.send_message(chat_id=CHAT_ID, text="❌ Aucun signal aujourd’hui. On reste patient.")
        return

    message = "🔥 Signaux du jour – CLUB SNIPER BANKS VIP 🔥\n\n"
    simples = matches[:2]
    combiné = matches[2:6]
    save_signals(simples + combiné)

    for m in simples:
        equipe_jouee = m["teams"].split("–")[0].strip()
        message += (
            f"{m['sport']}\n"
            f"💥 Match : {m['teams']}\n"
            f"🎯 Équipe à jouer : {equipe_jouee}\n"
            f"💰 Cote : {m['cote']}\n"
            f"🧠 Confiance : {round(min(m['cote'] / 2, 0.85) * 100)} %\n"
            f"💸 Mise : 2 %\n\n"
        )

    if combiné:
        total = 1
        message += "🔥 Combiné 🔥\n"
        for m in combiné:
            equipe_jouee = m["teams"].split("–")[0].strip()
            message += f"{m['sport']}\n🎯 {m['teams']} – Équipe à jouer : {equipe_jouee} – Cote : {m['cote']}\n"
            total *= m["cote"]
        message += f"\n💰 Total combiné : {round(total, 2)}\n🧠 Confiance : 76 %\n💸 Mise : 1.5 %"

    await bot.send_message(chat_id=CHAT_ID, text=message)

def auto_trigger_loop():
    while True:
        now = datetime.datetime.now(MONTREAL)
        if now.hour == 11 and now.minute == 30:
            loop.create_task(send_signals())
        time.sleep(60)

# === MAIN ===
if __name__ == "__main__":
    threading.Thread(target=auto_trigger_loop, daemon=True).start()
    loop.create_task(bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Le bot est actif et connecté !"))
    app.run(host="0.0.0.0", port=10000)
