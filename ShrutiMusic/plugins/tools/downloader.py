from pyrogram import filters
from pyrogram.types import Message
from ShrutiMusic import app
import requests
import os

@app.on_message(filters.command("vid"))
async def video_downloader(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a video URL.\n\nExample:\n/vid Any_video_url")

    video_url = message.text.split(None, 1)[1]

    msg = await message.reply("🔍 Fetching video...")

    # Step 1: Call API
    payload = {
        "url": video_url,
        "token": "c99f113fab0762d216b4545e5c3d615eefb30f0975fe107caab629d17e51b52d"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14)",
    }

    try:
        r = requests.post("https://allvideodownloader.cc/wp-json/aio-dl/video-data/", data=payload, headers=headers)
        data = r.json()

        if "medias" not in data or not data["medias"]:
            return await msg.edit("❌ No downloadable video found.")

        # Step 2: Get best quality video URL
        best_video = sorted(data["medias"], key=lambda x: x.get("quality", ""), reverse=True)[0]
        video_link = best_video["url"]

        # Step 3: Download the video to temp file
        await msg.edit("⬇️ Downloading video...")

        file_name = "video.mp4"
        with requests.get(video_link, stream=True) as v:
            with open(file_name, "wb") as f:
                for chunk in v.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Step 4: Send video to user
        await app.send_video(
            chat_id=message.chat.id,
            video=file_name,
            caption=f"🎬 {data.get('title', 'Video')}\n\n✅ ",
            supports_streaming=True
        )

        await msg.delete()
        os.remove(file_name)

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")

from pyrogram import filters
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShrutiMusic import app

from config import styled_button

REPO_VIDEO = "https://files.catbox.moe/x4x2e8.mp4"

@app.on_message(filters.command(["repo", "source"]))
async def send_repo(_, message: Message):
    await message.reply_video(
        video=REPO_VIDEO,
        caption=(
           "👑 <b>˹ ᴘʀɪᴠᴀᴛᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ˼</b>\n\n"
           "<blockquote>"
           "✨ <b>ʜᴇʏ ᴅᴇᴀʀ, ᴛʜᴇ ʀᴇᴘᴏꜱɪᴛᴏʀʏ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴘʀɪᴠᴀᴛᴇ ✨</b>\n\n"
           "🛒 <b>ᴛᴏ ᴘᴜʀᴄʜᴀꜱᴇ ᴛʜᴇ ʟᴀᴛᴇꜱᴛ ᴠᴇʀꜱɪᴏɴ, ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ!</b>\n\n"
           "🎁 <b>ᴄᴏɴᴛᴀᴄᴛ :</b> <a href='https://t.me/Villaiinn'>@V90001</a>"
           "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    styled_button(
                        "👑 Owner",
                        url="https://t.me/Villaiinn",
                        style=enums.ButtonStyle.PRIMARY,
                        icon_custom_emoji_id=6124902618574625426,
                    ),
                    styled_button(
                        "💸 Buy Now",
                        url="https://t.me/Villaiinnn",
                        style=enums.ButtonStyle.DANGER,
                        icon_custom_emoji_id=5409048419211682843,
                    )
                ]
            ]
        ),
        supports_streaming=True,
        has_spoiler=True,
    )

