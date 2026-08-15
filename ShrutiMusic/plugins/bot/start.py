import time

from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch
import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.plugins.sudo.sudoers import sudoers_list
from ShrutiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel_page1, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

from config import styled_button


def _make_start_text_pm(_, mention, bot_mention, UP=None, DISK=None, CPU=None, RAM=None):
    """Super premium private start message with gorgeous separate blockquotes."""
    return (
        f'<tg-emoji emoji-id="6231174832625552804">🦋</tg-emoji> ʜєʏ {mention},\n\n'
        f'<blockquote><b>ᴡєʟᴄᴏϻє ᴛᴏ {bot_mention} !</b></blockquote>\n'
        f'<blockquote><tg-emoji emoji-id="5913546818376964276">❤️</tg-emoji> ᴛʜɪs ɪs ϻυsɪᴄ ʙσᴛ\n'
        f'<tg-emoji emoji-id="6125239923831217642">✨</tg-emoji> ησ ʟᴧɢ | ᴧᴅs ϻυsɪᴄ | ησ ᴘʀσϻσ\n'
        f'<tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji> 24x7 ʀυη | ʙєsᴛ sσυηᴅ ǫυᴧʟɪᴛʏ</blockquote>\n'
        f'<blockquote><tg-emoji emoji-id="5271721134889395048">📼</tg-emoji> ᴜsᴇʀ: {mention}\n'
        f'<tg-emoji emoji-id="5429472766820628204">🕊</tg-emoji> ʙᴏᴛ ηᴧϻє: {bot_mention}</blockquote>\n'
        f'<blockquote><tg-emoji emoji-id="6231271181626903902">🎀</tg-emoji> ᴄʟɪᴄᴋ ση ᴛʜє ʜєʟᴩ ʙυᴛᴛση ᴛσ ɢєᴛ ɪηғσ ᴧʙσυᴛ ϻʏ ϻσᴅυʟєs ᴧηᴅ ᴄσϻϻᴧηᴅs...!</blockquote>\n\n'
        f'<tg-emoji emoji-id="6127558265573218459">💖</tg-emoji> ᴇɴᴊᴏʏ ɴᴏɴsᴛᴏᴘ ᴍᴜsɪᴄ ᴡɪᴛʜ {bot_mention}'
    )






def _make_start_text_group(_, bot_mention, uptime):
    """Rich group start message with blockquotes."""
    return (
        f"<b>🎵 {bot_mention} — Premium Music Bot</b>\n\n"
        f"<blockquote>✨ High-quality music streaming in your Voice Chat.</blockquote>\n"
        f"<blockquote>Supports YouTube • Spotify • Apple Music • SoundCloud • Telegram files.</blockquote>\n"
        f"<blockquote>⚡ Uptime: <code>{uptime}</code></blockquote>\n\n"
        f"<i>Use the buttons below to get started 👇</i>"
    )


async def send_start_media(message: Message, caption: str, reply_markup, media_url=None):
    url = media_url or config.START_IMG_URL
    is_video = False
    if url:
        clean_url = url.split("?")[0].lower()
        if clean_url.endswith((".mp4", ".mkv", ".webm", ".mov")):
            is_video = True

    # 1. Try sending with message_effect_id
    try:
        if is_video:
            return await message.reply_video(
                video=url,
                caption=caption,
                reply_markup=reply_markup,
                message_effect_id=5159385139981059251,
            )
        else:
            return await message.reply_photo(
                photo=url,
                caption=caption,
                reply_markup=reply_markup,
                message_effect_id=5159385139981059251,
            )
    except Exception:
        pass

    # 2. Try sending without message_effect_id
    try:
        if is_video:
            return await message.reply_video(
                video=url,
                caption=caption,
                reply_markup=reply_markup,
            )
        else:
            return await message.reply_photo(
                photo=url,
                caption=caption,
                reply_markup=reply_markup,
            )
    except Exception:
        pass

    # 3. Fallback: send as plain text
    try:
        return await message.reply_text(
            text=caption,
            reply_markup=reply_markup,
        )
    except Exception:
        pass


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel_page1(_)
            return await send_start_media(
                message=message,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                reply_markup=keyboard
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        styled_button(text=_["S_B_8"], url=link, style=enums.ButtonStyle.PRIMARY),
                        styled_button(text=_["S_B_9"], url=config.SUPPORT_GROUP, style=enums.ButtonStyle.PRIMARY),
                    ],
                ]
            )
            await m.delete()
            try:
                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                    message_effect_id=5159385139981059251,
                )
            except:
                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
        if name == "start":
            out = private_panel(_)
            UP, CPU, RAM, DISK = await bot_sys_stats()
            caption = _make_start_text_pm(
                _, message.from_user.mention, app.mention, UP, DISK, CPU, RAM
            )
            await send_start_media(
                message=message,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(out)
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        caption = _make_start_text_pm(
            _, message.from_user.mention, app.mention, UP, DISK, CPU, RAM
        )
        await send_start_media(
            message=message,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(out)
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    caption = _make_start_text_group(_, app.mention, get_readable_time(uptime))
    await send_start_media(
        message=message,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(out)
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                uptime = 0
                try:
                    uptime = int(time.time() - _boot_)
                except:
                    pass
                caption = _make_start_text_group(_, app.mention, get_readable_time(uptime))
                await send_start_media(
                    message=message,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(out)
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
