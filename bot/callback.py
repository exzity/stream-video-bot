from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import ASSISTANT_NAME as anime
from config import BOT_USERNAME as BUG

@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
  await query.edit_message_text(
    f"""ā HOW TO USE THIS BOT:

1.) first, add me to your group.
2.) then promote me as admin and give all permissions except anonymous admin.
3.) add @{anime} to your group.
4.) turn on the voice chat first before start to stream video.
5.) type /vplay (reply to video) to start streaming.
6.) type /end to end the video streaming.

š **note: stream & stop command can only be executed by group admin only!**

Powerd by @{BUG}""",
    reply_markup=InlineKeyboardMarkup(
      [[
        InlineKeyboardButton(
          "Close", callback_data="cls")
      ]]
    ))


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
  await query.edit_message_text(f"āØ **Hello there, I am a telegram video streaming bot.**\n\nš­ **I was created to stream videos in group video chats easily.**\n\nā **To find out how to use me, please press the help button below** šš»",
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
    f"""š All Command List:

Ā» /vplay (reply to video or file) - to stream video
Ā» /end - end the video streaming
Ā» /song (song name) - download song from YT
Ā» /vsong (video name) - download video from YT
Ā» /lyric (song name) - lyric scrapper

š° EXTRA CMD:

Ā» /alive - check bot alive status
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
