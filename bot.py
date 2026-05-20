import asyncio
import requests
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
import time

TOKEN = "6942005685:AAFKA-pFIzMhNIIhyErEeuB2B6LSz53qTrE"
CHAT_ID = None
KEYWORDS = ["stake", "sponsored", "drops", "rain", "casino", "slots"]

bot = Bot(token=TOKEN)

async def start(update: Update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    await update.message.reply_text("✅ Simple Kick Bot Started!\nI'll check every 60 seconds.")

async def check_kick():
    global CHAT_ID
    while True:
        try:
            r = requests.get("https://kick.com/api/v2/channels?limit=80", timeout=10)
            if r.status_code == 200:
                streams = r.json()
                for stream in streams[:60]:
                    slug = stream.get("slug", "")
                    if not slug:
                        continue
                    title = str(stream.get("title", "")).lower()
                    if any(kw in title for kw in KEYWORDS):
                        if slug not in globals().setdefault('last_alerted', set()):
                            globals()['last_alerted'].add(slug)
                            link = f"https://kick.com/{slug}"
                            msg = f"🔴 LIVE!\n{stream.get('title')}\n{link}"
                            if CHAT_ID:
                                await bot.send_message(chat_id=CHAT_ID, text=msg)
        except:
            pass
        await asyncio.sleep(60)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Start background checker
    asyncio.get_event_loop().create_task(check_kick())
    
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
