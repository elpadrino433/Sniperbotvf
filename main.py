import telegram
from flask import Flask

# Ton token et ton chat_id ici
BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = -1002840077042  # Remplace si nécessaire

# Création de l'application Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif."

@app.route('/test-signal')
def test_signal():
    bot = telegram.Bot(token=BOT_TOKEN)
    try:
        bot.send_message(chat_id=CHAT_ID, text="✅ TEST : Ceci est un signal envoyé par le bot.")
        return "✅ Message envoyé dans le groupe Telegram."
    except Exception as e:
        return f"❌ Erreur : {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
