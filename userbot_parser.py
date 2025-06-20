from telethon import TelegramClient, events
import aiohttp
import asyncio

API_ID = 20691763
API_HASH = '0721d0544c8162076d4b052e46b729ff'
BOT_API_TOKEN = '7977993721:AAEtw0ow9i30x_HK1cKlz74sjUwD3dFzHDQ'
TARGET_CHAT_ID = -1002414754875
KEYWORDS = [
    'сниму',
    'снимем',
    'нужна аренда',
    'нужна квартира',
    'ищу квартиру',
    'ищу кондо',
    'арендую'
]
SOURCE_CHATS = [
    '@pattayarental',
    '@Arenda_Pattaya',
    '@pattaya_arendaa',
    '@PattayaArenda',
    '@nedvizhimost_pattaya',
    '@baraholka_pattaya',
    '@baraholka_pattaya_ru',
    '@pattayan',
    '@pattaya_realty_estate',
    '@pattaya_realestate'
]

client = TelegramClient('userbot_session', API_ID, API_HASH)

async def send_to_bot(text, link):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": TARGET_CHAT_ID,
        "text": f"Найдено новое сообщение:\n\n{text}\n\n{link}",
        "disable_web_page_preview": True,
        "parse_mode": "HTML"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            if resp.status != 200:
                print(f"❌ Ошибка отправки: {resp.status}")
            else:
                print("✅ Сообщение отправлено")

@client.on(events.NewMessage(chats=SOURCE_CHATS))
async def handler(event):
    text = event.raw_text
    if any(keyword in text.lower() for keyword in KEYWORDS):
        chat = await event.get_chat()
        if getattr(chat, 'username', None):
            link = f"https://t.me/{chat.username}/{event.id}"
            await send_to_bot(text, link)

client.start()
print("✅ Userbot запущен и слушает каналы...")
client.run_until_disconnected()
