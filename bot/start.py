from time import time
from datetime import datetime
from helpers.filters import command
from helpers.decorators import sudo_users_only
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Chat, CallbackQuery
from config import BOT_USERNAME as Buu
from config import UPDATES_CHANNEL 
from config import SUPPORT_GROUP

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
      if m.chat.type == 'private':
           await m.reply(f"✨ **Hello there, I am a telegram video streaming bot.**\n\n💭 **I was created to stream videos in group video chats easily.**\n\n❔ **To find out how to use me, please press the help button below** 👇🏻",
                    reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "➕ Add me to your Group 🙋‍♀️", url=f"https://t.me/{Buu}?startgroup=true")
                       ],[
                          InlineKeyboardButton(
                             "🧰 HOW TO USE THIS BOT", callback_data="cbguide"),
                             
                          InlineKeyboardButton(
                             "🛠 Command List", callback_data="cblist")
                       ],[
                          InlineKeyboardButton(
                             "💭 Group", url="https://t.me/{SUPPORT_GROUP}"),
                          InlineKeyboardButton(
                             "📣 Channel", url="https://t.me/{UPDATES_CHANNEL}")
                       ]]
                    ))
   else:
      await m.reply("**I am alive now in your group ✅**",
                          reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "🧰 HOW TO USE THIS BOT 🛠 ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "🔎 Search Youtube", switch_inline_query='s ')
                       ],[
                          InlineKeyboardButton(
                             "🛠 Command List", callback_data="cblist")
                       ]]
                    )
      )


@Client.on_message(command(["help", f"help@{Buu}"]) & filters.group & ~filters.edited)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""🏃‍♂️**bot is running in your group ✅**\n<b>🤗**uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "🧰 HOW TO USE THIS BOT 🛠 ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "🔎 Search Youtube",  switch_inline_query_current_chat="")
                       ],[
                          InlineKeyboardButton(
                             "🛠 Command List", callback_data="cblist")
                       ]]
                    )
      )


@Client.on_message(command(["alive", f"alive@{Buu}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🤷‍♂️ bot status:\n"
        f"🙋‍♀️ `PONG!!`\n"
        f"✮✮ **Now online**`{delta_ping * 1000:.3f} ms`\n"
        f"✮✮ **Time Taken:** `{uptime}`\n"
        f"✮✮ **Service uptime:** `{START_TIME_ISO}`",
        reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "🧰 HOW TO USE THIS BOT 🛠 ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "🔎 Search Youtube",  switch_inline_query_current_chat="")
                       ],[
                          InlineKeyboardButton(
                             "🛠 Command List", callback_data="cblist")
                       ]]
                    )
    )
    
@Client.on_message(filters.regex("^!repo"))
async def repo(client, message):
    repo = "https://github.com/ImDenuwan/stream-video-bot"
    await message.reply(f"**Source code:** [Here]({repo})")