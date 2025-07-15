import datetime
import pytz
import telegram
import asyncio
from flask import Flask

BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = -1002840077042
MONTREAL = pytz.timezone("America/Montreal")

app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "Bot actif et prêt."

@app.route('/test-signal')
def test_signal():
    asyncio.run(envoi_signal_test())
    return "✅ Signal test envoyé."

async def envoi_signal_test():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot SNIPER.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
