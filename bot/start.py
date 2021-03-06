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
           await m.reply(f"āØ **Hello there, I am a telegram video streaming bot.**\n\nš­ **I was created to stream videos in group video chats easily.**\n\nā **To find out how to use me, please press the help button below** šš»",
                    reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "ā Add me to your Group šāāļø", url=f"https://t.me/{Buu}?startgroup=true")
                       ],[
                          InlineKeyboardButton(
                             "š§° HOW TO USE THIS BOT", callback_data="cbguide"),
                             
                          InlineKeyboardButton(
                             "š  Command List", callback_data="cblist")
                       ],[
                          InlineKeyboardButton(
                             "š­ Group", url="https://t.me/{SUPPORT_GROUP}"),
                          InlineKeyboardButton(
                             "š£ Channel", url="https://t.me/{UPDATES_CHANNEL}")
                       ]]
                    ))
   else:
      await m.reply("**I am alive now in your group ā**",
                          reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "š§° HOW TO USE THIS BOT š  ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "š Search Youtube", switch_inline_query='s ')
                       ],[
                          InlineKeyboardButton(
                             "š  Command List", callback_data="cblist")
                       ]]
                    )
      )


@Client.on_message(command(["help", f"help@{Buu}"]) & filters.group & ~filters.edited)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""šāāļø**bot is running in your group ā**\n<b>š¤**uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "š§° HOW TO USE THIS BOT š  ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "š Search Youtube",  switch_inline_query_current_chat="")
                       ],[
                          InlineKeyboardButton(
                             "š  Command List", callback_data="cblist")
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
        "š¤·āāļø bot status:\n"
        f"šāāļø `PONG!!`\n"
        f"ā®ā® **Now online**`{delta_ping * 1000:.3f} ms`\n"
        f"ā®ā® **Time Taken:** `{uptime}`\n"
        f"ā®ā® **Service uptime:** `{START_TIME_ISO}`",
        reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "š§° HOW TO USE THIS BOT š  ", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "š Search Youtube",  switch_inline_query_current_chat="")
                       ],[
                          InlineKeyboardButton(
                             "š  Command List", callback_data="cblist")
                       ]]
                    )
    )
    
@Client.on_message(filters.regex("^!repo"))
async def repo(client, message):
    repo = "https://github.com/ImDenuwan/stream-video-bot"
    await message.reply(f"**Source code:** [Here]({repo})")