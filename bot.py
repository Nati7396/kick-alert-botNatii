import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "6942005685:AAFKA-pFIzMhNIIhyErEeuB2B6LSz53qTrE"
CHAT_ID = None

KEYWORDS = ["stake", "sponsored", "#ad", "drops", "rain", "bonus", "casino", "slots"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

last_alerted = set()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    await message.answer("✅ Kick Sponsored Alert Bot is running!\n\nI'll check every 60 seconds for live Slots & Casino / Stake streams.")

async def check_live_streams():
    urls = [
        "https://kick.com/api/v2/channels?limit=100",
        "https://kick.com/api/v1/livestreams"
    ]
    
    for url in urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        continue
                    data = await resp.json()
                    
                    streams = data.get("data", []) if isinstance(data, dict) else data
                    
                    for stream in streams[:80]:
                        title = str(stream.get("title", "")).lower()
                        category = str(stream.get("category", "")).lower()
                        slug = stream.get("slug") or stream.get("channel", {}).get("slug", "")
                        
                        if not slug:
                            continue
                            
                        if any(kw in title or kw in category for kw in KEYWORDS):
                            stream_key = slug
                            if stream_key not in last_alerted:
                                last_alerted.add(stream_key)
                                link = f"https://kick.com/{slug}"
                                msg = f"🔴 **LIVE Sponsored Stream Detected!**\n\n**Title:** {stream.get('title')}\n**Category:** {category.title()}\n**Link:** {link}"
                                if CHAT_ID:
                                    await bot.send_message(CHAT_ID, msg)
        except:
            continue

async def background_task():
    while True:
        await check_live_streams()
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(background_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
