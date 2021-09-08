from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import ASSISTANT_NAME as anime
from config import BOT_USERNAME as BUG

@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""❓ HOW TO USE THIS BOT:

1.) first, add me to your group.
2.) then promote me as admin and give all permissions except anonymous admin.
3.) add @{anime} to your group.
4.) turn on the voice chat first before start to stream video.
5.) type /vplay (reply to video) to start streaming.
6.) type /end to end the video streaming.

📝 **note: stream & stop command can only be executed by group admin only!**

Powerd by @{BUG}""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "Close", callback_data="cls")
      ]]
    ))


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
  await query.edit_message_text(f"✨ **Hello there, I am a telegram video streaming bot.**\n\n💭 **I was created to stream videos in group video chats easily.**\n\n❔ **To find out how to use me, please press the help button below** 👇🏻",
                                reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "HOW TO USE THIS BOT", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             " All Command List", callback_data="cblist")
                       ]]
                    ))

@Client.on_callback_query(filters.regex("cblist"))
async def cblist(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""📚 All Command List:

» /vplay (reply to video or file) - to stream video
» /end - end the video streaming
» /song (song name) - download song from YT
» /vsong (video name) - download video from YT
» /lyric (song name) - lyric scrapper

🔰 EXTRA CMD:

» /alive - check bot alive status
Powerd by @szrosebot""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "close", callback_data="cls")
      ]]
    ))


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    await query.message.delete()
