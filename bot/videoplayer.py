import os
import re
import pafy
import time
import asyncio
import ffmpeg
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from youtube_dl import YoutubeDL
from pytube import YouTube
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch

from config import API_ID, API_HASH, SESSION_NAME, BOT_USERNAME
from helpers.decorators import authorized_users_only
from helpers.filters import command

ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)

STREAM = {8}
VIDEO_CALL = {}

app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)



def video_link_getter(url: str, key=None):
    try:
        yt = YouTube(url)
        if key == "v":
            x = yt.streams.filter(file_extension="mp4", res="460p")[0].download()
        elif key == "a":
            x = yt.streams.filter(type="audio")[-1].download()
        return x
    except Exception as e:
        print(str(e))
        return 500

def yt_video_search(q: str):
    try:
        videosSearch = VideosSearch(q, limit=1)
        videoSearchId = videosSearch.result()['result'][0]['id']
        finalurl = f"https://www.youtube.com/watch?v={videoSearchId}"
        return finalurl
    except:
        return 404

@Client.on_message(command(["vstop", f"vstop@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def leave_vc(client, message):
    CHAT_ID = message.chat.id
    user = message.from_user.mention
    if not str(CHAT_ID).startswith("-100"): return
    try:
        await message.delete()
        await VIDEO_CALL[CHAT_ID].stop()
        await message.reply("✅ **streaming has ended successfully !\n\n» Stopped by {user}**")
    except: pass

@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def play_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("🔁 __Processing.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a  video or  youtube URL or Search Query.")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("__No videos found__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="a")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
        user = message.from_user.mention
    try:
        group_call = group_call_factory.get_group_call()
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Playing...__\n\n» join to video chat on the top to watch streaming.")
        await group_call.start_audio(LOCAL_FILE, repeat=False)
        VIDEO_CALL[CHAT_ID] = group_call
        await msg.delete()
        await message.reply_photo(
                    photo="./bot/Test.png",
                    caption=f"**Started Video Streaming !**\n**Request by:** {user}\n**To stop:** /vstop",
                )

    except Exception as e:
        await message.reply(str(e))
        return await VIDEO_CALL[CHAT_ID].stop()


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def stream_vc(client, message):
    CHAT_ID = message.chat.id
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a  video or  youtube URL or Search Query.")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("__No videos found__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="v")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
        user = message.from_user.mention
    try:
        group_call = group_call_factory.get_group_call()
        if group_call.is_connected: await group_call.stop()
        await group_call.join(CHAT_ID)
        await msg.edit("🚩 __Playing...__\n\n» join to video chat on the top to watch streaming.")
        await group_call.start_video(LOCAL_FILE, repeat=False)
        VIDEO_CALL[CHAT_ID] = group_call
        await msg.delete()
        await message.reply_photo(
                    photo="./bot/Test.png",
                    caption=f"**Started Video Streaming !**\n**Request by:** {user}\n**To stop:** /vstop",
                )
    except Exception as e:
        await message.reply(str(e))
        return await VIDEO_CALL[CHAT_ID].stop()

Client.run()
