import re
import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from ..logging import LOGGER
from config import styled_button

OWNER_IS_PREMIUM = True

EMOJI_PREMIUM_MAP = {
    "⏱": 5458640241915084025,
    "✨": 6111831431070094156,
    "💕": 6228486964782305310,
    "💫": 5814662983162270430,
    "🎶": 5814498932591432312,
    "👋": 5413694143601842851,
    "🎵": 6237500542063481886,
    "🎄": 4958563601775330153,
    "➡️": 4956282853882069908,
    "⛔": 5415748817301555221,
    "📊": 5416083837635543767,
    "📌": 5388951150542218857,
    "⏳": 5386367538735104399,
    "➕": 5420163708674384414,
    "▶️": 5334885900356688822,
    "🙂": 5461117441612462242,
    "☄️": 5224607267797606837,
    "🛍": 5229064374403998351,
    "🚫": 5240241223632954241,
    "‼️": 5440660757194744323,
    "⁉️": 5314504236132747481,
    "❓": 5436113877181941026,
    "⚠️": 5447644880824181073,
    "🔴": 5420323339723881652,
    "🌐": 5447410659077661506,
    "💬": 6228671708505575110,
    "💭": 5467538555158943525,
    "✔️": 5206607081334906820,
    "❌": 5210952531676504517,
    "🔔": 5458603043203327669,
    "📌": 5397782960512444700,
    "🏷": 5397782960512444700,
    "💵": 5409048419211682843,
    "💸": 5233326571099534068,
    "➡️": 5416117059207572332,
    "🔥": 5424972470023104089,
    "💥": 5276032951342088188,
    "👍": 5337080053119336309,
    "👎": 5449875686837726134,
    "🛡": 5251203410396458957,
    "🛡️": 5251203410396458957,
    "🔗": 5271604874419647061,
    "🖥": 5282843764451195532,
    "ℹ️": 5334544901428229844,
    "ℹ": 5334544901428229844,
    "🔄": 5375338737028841420,
    "✨": 6111831431070094156,
    "🥀": 6125239923831217642,
    "👑": 6124902618574625426,
    "💎": 6228499360057922405,
    "✉️": 5253742260054409879,
    "✉": 5253742260054409879,
    "🔒": 5296369303661067030,
    "⚙️": 5341715473882955310,
    "⚙": 5341715473882955310,
    "⌛️": 5386367538735104399,
    "⌛": 5386367538735104399,
    "⚡️": 6124898345082165755,
    "⚡": 6124898345082165755,
    "✧": 5944857705490419986,
    "❖": 5458603043203327669,
    "➤": 5416117059207572332,
    "✦": 5944857705490419986,
    "➥": 5416117059207572332,
    "➲": 5416117059207572332,
    "➻": 5416117059207572332,
    "👤": 5373012449597335010,
    "🎧": 5814498932591432312,
    "📜": 5253742260054409879,
    "🇮🇳": 5447410659077661506,
    "♪": 5814498932591432312,
    "🥂": 5260567255145539253,
    "🔙": 5416117059207572332,
    "📢": 5458603043203327669,
    "📣": 5458603043203327669,
    "📲": 5282843764451195532,
    "👀": 5210956306952758910,
    "😄": 6124985528623306624,
    "🧋": 6066829481002146041,
    "🫶": 5285338659413846416,
    "🥳": 6127220625309177529,
    "🍟": 6066424010319599691,
    "🎇": 6199293238847740460,
    "💘": 6114138580127322092,
    "❤️": 6228606996233327076,
    "❤": 5913546818376964276,
    "🍭": 6174884334114182449,
    "💝": 5280826864988873394,
    "🎭": 5276239041052828276,
    "⭐️": 5289944036881230584,
    "⭐": 5289944036881230584,
    "🔑": 5278573677900752088,
    "💞": 5220069080798611448,
    "💖": 5303310030940952439,
    "🎉": 5235711785482341993,
    "💗": 6226386317752668627,
    "🎵": 5348201978306509336,
    "🎤": 5224736245665511429,
    "🎁": 5886694236165773623,
    "🚀": 5355332431471748210,
    "🍦": 5899828662768769578,
    "📊": 5357436596079592754,
    "🎄": 4958563601775330153,
    "⏱": 5458640241915084025,
    "👋": 5413694143601842851,
    "📂": 5357315181649076022,
    "📩": 5253742260054409879,
    "💕": 6228486964782305310,
    "💫": 5814662983162270430,
    "🎶": 5814498932591432312,
    "🌸": 6203732770447954405,
    "📦": 6005639597332110711,
    "📼": 5271721134889395048,
    "🥇": 5217504976732961241,
    "🤞": 5427078438517218023,
    "🕯": 5458681954637458966,
    "🍔": 5201713249568960832,
    "😇": 5454238639171056478,
    "😚": 5429400692974435020,
    "😊": 5402549639771596623,
    "😮": 5303479226882603449,
    "🚩": 5460755126761312667,
    "🤙": 6125098305874564832,
    "➡️": 5416117059207572332,
    "⬅️": 6125103558619568255,
    "🦁": 6159124780550200563,
    "🎼": 6291574588342016102,
    "😧": 5872945886937487933,
    "😎": 5868616723111876962,
    "🐦": 5429472766820628204,
    "🫰": 6178999423884858274,
    "🔊": 5814498932591432312,
    "🎥": 5271721134889395048,
    "🔍": 5436113877181941026,
    "🗄️": 5357315181649076022,
    "🗄": 5357315181649076022,
    "🛒": 5229064374403998351,
    "🌿": 5882057217674321163,
    "🌱": 5882057217674321163,
    "🍃": 5882057217674321163,
    "🔈": 5388632425314140043,
    "🥰": 6228883566357386014,
    "😍": 5458696196749008675,
    "🧩": 5265120027853481187,
    "⭐️": 5289944036881230584,
    "⭐": 5267500801240092311,
    "☁️": 5274002879215067737,
    "☁": 5274002879215067737,
    "💭": 5467538555158943525,
    "📣": 5424818078833715060,
    "🔖": 5222444124698853913,
    "🎙": 5294339927318739359,
    "🔥": 5424972470023104089,
    "🌛": 5449569374065152798,
    "🏠": 5416041192905265756,
    "🌎": 5224450179368767019,
    "🛫": 5201691993775818138,
    "🪙": 5298719183347932250,
    "🐴": 5254002689691375922,
    "🕺": 5312417646531073538,
    "🏊‍♀️": 5273999868442989248,
    "🏊": 5273999868442989248,
    "🏹": 5215498441026720661,
    "🥉": 5266998599304104035,
    "🚴": 5242347299501267412,
    "🎀": 6230928778244132065,
    "🌹": 5882057217674321163,
    "💌": 5253742260054409879,
    "📥": 5357315181649076022,
    "📤": 5357315181649076022,
    "📖": 5253742260054409879,
    "📚": 5253742260054409879,
    "🏆": 5217504976732961241,
    "💡": 5456140674028019486,
    "🕊️": 5429472766820628204,
    "🕊": 5429472766820628204,
    "💸": 5409048419211682843,
    "🔤": 5253742260054409879,
    "🎨": 6125239923831217642,
    "🤬": 5872945886937487933,
    "😤": 5872945886937487933,
    "💢": 5424972470023104089,
    "🤖": 5282843764451195532,
    "🎯": 5427168083074628963,
    "📋": 5253742260054409879,
    "📝": 5253742260054409879,
    "🔧": 5341715473882955310,
    "🌟": 6125239923831217642,
    "🌅": 5882057217674321163,
    "☀️": 6125239923831217642,
    "🛑": 5240241223632954241,
    "🌞": 6125239923831217642,
    "🌤️": 5274002879215067737,
    "🌤": 5274002879215067737,
    "🌙": 5449569374065152798,
    "🌜": 5449569374065152798,
    "📌": 5397782960512444700,
    "💑": 6127558265573218459,
    "💏": 6127558265573218459,
    "📸": 5271721134889395048,
    "🖼️": 6125239923831217642,
    "🖼": 6125239923831217642,
    "📅": 5458640241915084025,
    "🔹": 5416117059207572332,
    "㋛": 5461117441612462242,
    "💞": 6127558265573218459,
    "🏅": 5217504976732961241,
    "💾": 5357315181649076022,
    "😅": 5461117441612462242,
    "💪": 5456140674028019486,
    "⏰": 5458640241915084025,
    "🐰": 6226523395928887418,
    "✌": 6228931360753455512,
    "🙃": 6226371238122491635,
    "🤍": 6228905681143993219,
    "🤩": 6226508818809885268,
    "😞": 6226602436212036422,
    "🛌": 6230798872663297567,
    "😽": 6228492397915934857,
    "🦋": 6228999461754900766,
    "❤️🔥": 6204218161881944539,
    "💓": 6203994196517327435,
    "😴": 6204050267315376719,
}


def transform_custom_emojis(text: str) -> str:
    """
    Converts standard emojis to Telegram premium animated custom emojis.
    Only applies if the bot owner has Telegram Premium (OWNER_IS_PREMIUM=True).
    Also handles markdown shorthand: ![emoji](tg://emoji?id=12345)
    """
    if not text or not isinstance(text, str):
        return text
    # Always process markdown shorthand
    text = re.sub(r'!\[(.*?)\]\(tg://emoji\?id=(\d+)\)', r'<tg-emoji emoji-id="\2">\1</tg-emoji>', text)
    
    # Only inject premium emoji tags when owner is premium
    if OWNER_IS_PREMIUM:
        placeholders = {}
        def save_tag(match):
            idx = f"__TGE_{len(placeholders)}__"
            placeholders[idx] = match.group(0)
            return idx
            
        # Temporarily remove existing tg-emoji tags to avoid nested replacements
        text = re.sub(r'<tg-emoji[^>]*>.*?</tg-emoji>', save_tag, text)
        
        for emoji, emoji_id in sorted(EMOJI_PREMIUM_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            if emoji in text:
                text = text.replace(emoji, f'<tg-emoji emoji-id="{emoji_id}">{emoji}</tg-emoji>')
                
        # Restore tags
        for idx, tag in placeholders.items():
            text = text.replace(idx, tag)
            
    return text



class Nand(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting bot...")
        super().__init__(
            name="ShrutiMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def send_message(self, chat_id, text="", *args, **kwargs):
        if "text" in kwargs:
            kwargs["text"] = transform_custom_emojis(kwargs["text"])
        elif text:
            text = transform_custom_emojis(text)
        return await super().send_message(chat_id, text, *args, **kwargs)

    async def edit_message_text(self, chat_id, message_id, text="", *args, **kwargs):
        msg_text = kwargs.get("text", text)
        msg_text = transform_custom_emojis(msg_text)
        if "text" in kwargs:
            kwargs["text"] = msg_text
        else:
            text = msg_text
        try:
            return await super().edit_message_text(chat_id, message_id, text, *args, **kwargs)
        except Exception as e:
            try:
                new_kwargs = kwargs.copy()
                if "text" in new_kwargs:
                    del new_kwargs["text"]
                return await self.edit_message_caption(chat_id, message_id, caption=msg_text, *args, **new_kwargs)
            except Exception:
                raise e

    async def send_photo(self, chat_id, photo, caption="", *args, **kwargs):
        kwargs["has_spoiler"] = True
        if "caption" in kwargs:
            kwargs["caption"] = transform_custom_emojis(kwargs["caption"])
        elif caption:
            caption = transform_custom_emojis(caption)

        import os
        photo_val = kwargs.get("photo", photo)
        if isinstance(photo_val, str):
            clean_url = photo_val.split('?')[0].lower()
            if clean_url.endswith((".mp4", ".mkv", ".webm", ".mov")):
                if "photo" in kwargs:
                    del kwargs["photo"]
                return await self.send_video(chat_id, video=photo_val, caption=caption, *args, **kwargs)

            photo_val = photo_val.replace("\\", "/")
            if not photo_val.startswith(("http://", "https://")):
                if os.path.exists(photo_val):
                    opened_file = open(photo_val, "rb")
                    if "photo" in kwargs:
                        kwargs["photo"] = opened_file
                    else:
                        photo = opened_file
        return await super().send_photo(chat_id, photo, caption, *args, **kwargs)

    async def send_video(self, chat_id, video, caption="", *args, **kwargs):
        kwargs["has_spoiler"] = True
        if "caption" in kwargs:
            kwargs["caption"] = transform_custom_emojis(kwargs["caption"])
        elif caption:
            caption = transform_custom_emojis(caption)

        import os
        video_val = kwargs.get("video", video)
        if isinstance(video_val, str):
            video_val = video_val.replace("\\", "/")
            if not video_val.startswith(("http://", "https://")):
                if os.path.exists(video_val):
                    opened_file = open(video_val, "rb")
                    if "video" in kwargs:
                        kwargs["video"] = opened_file
                    else:
                        video = opened_file
        return await super().send_video(chat_id, video, caption, *args, **kwargs)

    async def edit_message_caption(self, chat_id, message_id, caption="", *args, **kwargs):
        if "caption" in kwargs:
            kwargs["caption"] = transform_custom_emojis(kwargs["caption"])
        elif caption:
            caption = transform_custom_emojis(caption)
        return await super().edit_message_caption(chat_id, message_id, caption, *args, **kwargs)

    async def edit_message_media(self, chat_id, message_id, media, *args, **kwargs):
        if media:
            media.has_spoiler = True
            if getattr(media, "caption", None):
                media.caption = transform_custom_emojis(media.caption)
        return await super().edit_message_media(chat_id, message_id, media, *args, **kwargs)

    async def send_audio(self, chat_id, audio, caption="", *args, **kwargs):
        if "caption" in kwargs:
            kwargs["caption"] = transform_custom_emojis(kwargs["caption"])
        elif caption:
            caption = transform_custom_emojis(caption)
        return await super().send_audio(chat_id, audio, caption, *args, **kwargs)

    async def send_document(self, chat_id, document, caption="", *args, **kwargs):
        if "caption" in kwargs:
            kwargs["caption"] = transform_custom_emojis(kwargs["caption"])
        elif caption:
            caption = transform_custom_emojis(caption)
        return await super().send_document(chat_id, document, caption, *args, **kwargs)


    async def start(self):
        global OWNER_IS_PREMIUM
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        OWNER_IS_PREMIUM = True
        LOGGER(__name__).info("Owner Premium Status forced to: True")


        button = InlineKeyboardMarkup(
            [
                [
                    styled_button(
                        text="Add Me To Your Group",
                        url=f"https://t.me/{self.username}?startgroup=true",
                        style="success",
                    )
                ]
            ]
        )

        if config.LOG_GROUP_ID:
            try:
                await self.send_video(
                    config.LOG_GROUP_ID,
                    video=config.START_IMG_URL,
                    caption=f"<b>🎵 Bot Started Successfully</b>\n\n"
                            f"<b>Name:</b> {self.name}\n"
                            f"<b>Username:</b> @{self.username}\n"
                            f"<b>ID:</b> <code>{self.id}</code>\n\n"
                            f"<i>Bot is now online and ready to serve!</i>",
                    reply_markup=button,
                )
            except pyrogram.errors.ChatWriteForbidden:
                LOGGER(__name__).error("Bot cannot write to the log group")
            except Exception as e:
                LOGGER(__name__).error(f"Error while sending to log group: {e}")

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
