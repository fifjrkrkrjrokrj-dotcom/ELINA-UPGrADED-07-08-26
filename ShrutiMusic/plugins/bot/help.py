from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

def format_help_text(text: str) -> str:
    text = text.strip()
    if "\n\n" in text:
        parts = text.split("\n\n", 1)
        heading = parts[0].strip()
        body = parts[1].strip()
        
        # Add cool emojis in front of headings
        if "ᴀᴅᴍɪɴ" in heading:
            heading = f'<tg-emoji emoji-id="5251203410396458957">🛡️</tg-emoji> {heading}'
        elif "ᴘɪɴɢ" in heading or "sᴛᴀᴛs" in heading:
            heading = f'<tg-emoji emoji-id="5355332431471748210">🚀</tg-emoji> {heading}'
        elif "ᴩʟᴀʏ" in heading or "ᴘʟᴀʏ" in heading:
            heading = f'<tg-emoji emoji-id="5348201978306509336">🎵</tg-emoji> {heading}'
        elif "ᴀᴜᴛʜ" in heading:
            heading = f'<tg-emoji emoji-id="6124902618574625426">👑</tg-emoji> {heading}'
        elif "ғᴏʀᴄᴇ" in heading or "ғsᴜʙ" in heading or "sᴜʙsᴄʀɪᴘᴛɪᴏɴ" in heading:
            heading = f'<tg-emoji emoji-id="5296369303661067030">🔒</tg-emoji> {heading}'
        elif "ʟᴏᴏᴘ" in heading:
            heading = f'<tg-emoji emoji-id="5449569374065152798">🌛</tg-emoji> {heading}'
        elif "ɢᴀᴍᴇs" in heading:
            heading = f'<tg-emoji emoji-id="6127220625309177529">🥳</tg-emoji> {heading}'
        elif "ᴅᴏᴡɴʟᴏᴀᴅ" in heading:
            heading = f'<tg-emoji emoji-id="5886694236165773623">🎁</tg-emoji> {heading}'
        elif "ɪɴғᴏʀᴍᴀᴛɪᴏɴ" in heading or "ɪɴғᴏ" in heading:
            heading = f'<tg-emoji emoji-id="5357436596079592754">📊</tg-emoji> {heading}'
        elif "ᴛᴀɢ" in heading:
            heading = f'<tg-emoji emoji-id="5460755126761312667">🚩</tg-emoji> {heading}'
        else:
            heading = f'<tg-emoji emoji-id="6125239923831217642">✨</tg-emoji> {heading}'
            
        # Format the command lines in body with cool bullet points (💎)
        formatted_lines = []
        for line in body.split("\n"):
            line_str = line.strip()
            if line_str.startswith("/"):
                # Use diamond premium emoji as command bullet point
                formatted_lines.append(f'<tg-emoji emoji-id="5427168083074628963">💎</tg-emoji> {line_str}')
            elif line_str:
                # Replace standard emojis in the explanation text too!
                line_str = line_str.replace("🗄️", '<tg-emoji emoji-id="5357315181649076022">🗄️</tg-emoji>')
                line_str = line_str.replace("🗄", '<tg-emoji emoji-id="5357315181649076022">🗄</tg-emoji>')
                line_str = line_str.replace("🎁", '<tg-emoji emoji-id="5886694236165773623">🎁</tg-emoji>')
                line_str = line_str.replace("🪙", '<tg-emoji emoji-id="5298719183347932250">🪙</tg-emoji>')
                line_str = line_str.replace("🎀", '<tg-emoji emoji-id="6231271181626903902">🎀</tg-emoji>')
                line_str = line_str.replace("🌹", '<tg-emoji emoji-id="5882057217674321163">🌹</tg-emoji>')
                line_str = line_str.replace("💌", '<tg-emoji emoji-id="5253742260054409879">💌</tg-emoji>')
                line_str = line_str.replace("📖", '<tg-emoji emoji-id="5253742260054409879">📖</tg-emoji>')
                line_str = line_str.replace("📚", '<tg-emoji emoji-id="5253742260054409879">📚</tg-emoji>')
                line_str = line_str.replace("🏆", '<tg-emoji emoji-id="5217504976732961241">🏆</tg-emoji>')
                line_str = line_str.replace("💡", '<tg-emoji emoji-id="5456140674028019486">💡</tg-emoji>')
                line_str = line_str.replace("🕊️", '<tg-emoji emoji-id="5429472766820628204">🕊️</tg-emoji>')
                line_str = line_str.replace("🕊", '<tg-emoji emoji-id="5429472766820628204">🕊</tg-emoji>')
                line_str = line_str.replace("💸", '<tg-emoji emoji-id="5409048419211682843">💸</tg-emoji>')
                formatted_lines.append(line_str)
        formatted_body = "\n".join(formatted_lines)
            
        return f"<blockquote>{heading}</blockquote>\n\n<blockquote>{formatted_body}</blockquote>"
    return f"<blockquote>{text}</blockquote>"




from ShrutiMusic import app
from ShrutiMusic.utils.database import get_lang
from ShrutiMusic.utils.decorators.language import LanguageStart, languageCB
from ShrutiMusic.utils.inline.help import (
    help_back_markup,
    private_help_panel,
    help_pannel_page1,
    help_pannel_page2,
    help_pannel_page3,
    help_pannel_page4,
)
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_GROUP
from strings import get_string, helpers

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
async def helper_private(
    client: app, update: types.Message
):
    try:
        await update.delete()
    except:
        pass
    language = await get_lang(update.chat.id)
    _ = get_string(language)
    keyboard = help_pannel_page1(_)
    
    url = HELP_IMG_URL
    is_video = url.split("?")[0].lower().endswith((".mp4", ".mkv", ".webm", ".mov")) if url else False
    
    try:
        if is_video:
            await update.reply_video(
                video=url,
                caption=_["help_1"].format(SUPPORT_GROUP),
                reply_markup=keyboard,
            )
        else:
            await update.reply_photo(
                photo=url,
                caption=_["help_1"].format(SUPPORT_GROUP),
                reply_markup=keyboard,
            )
    except Exception:
        try:
            await update.reply_text(
                text=_["help_1"].format(SUPPORT_GROUP),
                reply_markup=keyboard,
            )
        except Exception:
            pass

@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    # Helper to return keyboard with correct page
    def get_keyboard_for(cb):
        page1 = ["hb1", "hb2", "hb3", "hb4", "hb5", "hb6", "hb7", "hb8", "hb9", "hb10"]
        page2 = ["hb11", "hb12", "hb13", "hb14", "hb15", "hb17", "hb18", "hb19", "hb20", "hb21"]
        page3 = ["hb22", "hb23", "hb24", "hb25", "hb26", "hb27", "hb28", "hb29", "hb30", "hb31"]
        page4 = ["hb32", "hb33", "hb34", "hb35", "hb36", "hb37", "hb38", "hb39"]

        if cb in page1:
            return help_back_markup(_, page=1)
        elif cb in page2:
            return help_back_markup(_, page=2)
        elif cb in page3:
            return help_back_markup(_, page=3)
        elif cb in page4:
            return help_back_markup(_, page=4)
    # Dictionary mapping callback data to help content
    help_map = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
        "hb16": helpers.HELP_16,
        "hb17": helpers.HELP_17,
        "hb18": helpers.HELP_18,
        "hb19": helpers.HELP_19,
        "hb20": helpers.HELP_20,
        "hb21": helpers.HELP_21,
        "hb22": helpers.HELP_22,
        "hb23": helpers.HELP_23,
        "hb24": helpers.HELP_24,
        "hb25": helpers.HELP_25,
        "hb26": helpers.HELP_26,
        "hb27": helpers.HELP_27,
        "hb28": helpers.HELP_28,
        "hb29": helpers.HELP_29,
        "hb30": helpers.HELP_30,
        "hb31": helpers.HELP_31,
        "hb32": helpers.HELP_32,
        "hb33": helpers.HELP_33,
        "hb34": helpers.HELP_34,
        "hb35": helpers.HELP_35,
        "hb36": helpers.HELP_36,
        "hb37": helpers.HELP_37,
        "hb38": helpers.HELP_38,
        "hb39": helpers.HELP_39,
    }

    if cb in help_map:
        text = help_map[cb]
        wrapped_text = format_help_text(text)
        try:
            await CallbackQuery.message.edit_caption(
                caption=wrapped_text,
                reply_markup=get_keyboard_for(cb)
            )
        except Exception:
            try:
                await CallbackQuery.edit_message_text(
                    text=wrapped_text,
                    reply_markup=get_keyboard_for(cb)
                )
            except Exception:
                pass

