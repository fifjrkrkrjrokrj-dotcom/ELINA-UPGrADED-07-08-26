from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.core.call import Nand
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    url = PING_IMG_URL
    is_video = url.split("?")[0].lower().endswith((".mp4", ".mkv", ".webm", ".mov")) if url else False

    if is_video:
        response = await message.reply_video(
            video=url,
            caption=_["ping_1"].format(app.mention),
        )
    else:
        response = await message.reply_photo(
            photo=url,
            caption=_["ping_1"].format(app.mention),
        )

    pytgping = await Nand.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()

    resp = (datetime.now() - start).total_seconds() * 1000

    await response.edit_caption(
        caption=_["ping_2"].format(
            round(resp, 2),
            app.mention,
            UP,
            RAM,
            CPU,
            DISK,
            pytgping,
        ),
        reply_markup=supp_markup(_),
    )
