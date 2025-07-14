import telegram

BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = '@tUl5IOp8c8dhM2Nh'

message = """
🔥 Signal de test – CLUB SNIPER BANKS VIP 🔥

💥 PSG vs Lyon  
💰 Cote : 1.72  
🧠 Confiance : 84 %  
💸 Mise : 2 %

🔥 Combiné 🔥  
⚾ Yankees vs Red Sox – 1.65  
🏀 Lakers vs Celtics – 1.70  
💰 Total combiné : 2.81  
🧠 Confiance : 76 %  
💸 Mise : 1.5 %
"""

try:
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)
    print("✅ Message envoyé avec succès !")
except Exception as e:
    print(f"❌ Erreur : {e}")
