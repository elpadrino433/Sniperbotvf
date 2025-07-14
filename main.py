import asyncio
from telegram import Bot

BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'
CHAT_ID = '@tUl5IOp8c8dhM2Nh'

async def send_test_signal():
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
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_test_signal())
