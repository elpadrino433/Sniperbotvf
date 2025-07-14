from telegram.ext import Application, MessageHandler, filters
from telegram import Update
import asyncio

BOT_TOKEN = '8180955487:AAGlr_vepQIG71ecJB9dqPquDhdgbth7fx0'

async def get_chat_id(update: Update, context):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"✅ Ton chat ID est : `{chat_id}`", parse_mode='Markdown')

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, get_chat_id))
    app.run_polling()

if __name__ == "__main__":
    main()
