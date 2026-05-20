import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "6942005685:AAFKA-pFIzMhNIIhyErEeuB2B6LSz53qTrE"
CHAT_ID = None

KEYWORDS = ["stake", "sponsored", "#ad", "drops", "rain", "casino", "slots", "bonus"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

last_alerted = set()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    await message.answer("✅ Kick Alert Bot is now running!\nChecking every 60 seconds.")

async def check_live_streams():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://kick.com/api/v2/channels?limit=100", timeout=15) as resp:
                if resp.status != 200:
                    return
                data = await resp.json()
                
                streams = data if isinstance(data, list) else data.get("data", data.get("channels", []))
                
                for stream in streams[:80]:
                    slug = stream.get("slug") or ""
                    if not slug:
                        continue
                    title = str(stream.get("title", "")).lower()
                    category = str(stream.get("category", "")).lower()
                    
                    if any(kw in title or kw in category for kw in KEYWORDS):
                        if slug not in last_alerted:
                            last_alerted.add(slug)
                            link = f"https://kick.com/{slug}"
                            msg = f"🔴 **LIVE Sponsored Stream!**\n\nTitle: {stream.get('title')}\nCategory: {category}\n🔗 {link}"
                            if CHAT_ID:
                                await bot.send_message(CHAT_ID, msg)
    except Exception:
        pass

async def background_task():
    while True:
        await check_live_streams()
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(background_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
